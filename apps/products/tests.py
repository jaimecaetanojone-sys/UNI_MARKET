from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ModelTests(TestCase):
    def test_category_slug_is_generated(self):
        category = Category.objects.create(name="Material Escolar")
        self.assertEqual(category.slug, "material-escolar")

    def test_price_uses_decimal_and_rejects_zero(self):
        category = Category.objects.create(name="Livros")
        product = Product(category=category, name="X", price=Decimal("0.00"))
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_in_stock_property(self):
        category = Category.objects.create(name="Livros")
        self.assertFalse(Product(category=category, name="A", price="1.00", stock=0).in_stock)
        self.assertTrue(Product(category=category, name="B", price="1.00", stock=3).in_stock)


class ProductPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.books = Category.objects.create(name="Livros")
        cls.tech = Category.objects.create(name="Tecnologia")
        cls.book = Product.objects.create(category=cls.books, name="Física Geral", price="200.00", stock=1)
        cls.phone = Product.objects.create(category=cls.tech, name="Telemóvel usado", price="4500.00", stock=1)
        cls.hidden = Product.objects.create(category=cls.books, name="Inativo", price="50.00", is_active=False)

    def test_list_search_filters_by_text(self):
        response = self.client.get(reverse("products:list"), {"q": "Física"})
        self.assertContains(response, "Física Geral")
        self.assertNotContains(response, "Telemóvel usado")

    def test_list_filters_by_category(self):
        response = self.client.get(reverse("products:list"), {"categoria": "tecnologia"})
        self.assertContains(response, "Telemóvel usado")
        self.assertNotContains(response, "Física Geral")

    def test_list_filters_by_price_range(self):
        response = self.client.get(reverse("products:list"), {"preco_min": "1000"})
        self.assertContains(response, "Telemóvel usado")
        self.assertNotContains(response, "Física Geral")

    def test_invalid_price_filter_is_ignored(self):
        response = self.client.get(reverse("products:list"), {"preco_min": "abc"})
        self.assertEqual(response.status_code, 200)

    def test_no_results_shows_empty_state(self):
        response = self.client.get(reverse("products:list"), {"q": "inexistente"})
        self.assertContains(response, "Nenhum produto encontrado")

    def test_inactive_products_are_not_listed_nor_viewable(self):
        self.assertNotContains(self.client.get(reverse("products:list")), "Inativo")
        response = self.client.get(reverse("products:detail", args=[self.hidden.pk]))
        self.assertEqual(response.status_code, 404)

    def test_detail_page(self):
        response = self.client.get(reverse("products:detail", args=[self.book.pk]))
        self.assertContains(response, "Física Geral")
        self.assertContains(response, "200,00 MT")


class CategoryApiTests(TestCase):
    def test_list_is_public_and_only_active(self):
        Category.objects.create(name="Livros")
        Category.objects.create(name="Arquivada", is_active=False)
        response = self.client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, 200)
        names = [item["name"] for item in response.json()]
        self.assertEqual(names, ["Livros"])

    def test_write_methods_are_not_allowed(self):
        response = self.client.post("/api/v1/categories/", {"name": "Nova"})
        self.assertEqual(response.status_code, 405)

    def test_swagger_docs_load(self):
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)
        self.assertEqual(self.client.get("/api/schema/").status_code, 200)
