from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product


class HomePageTests(TestCase):
    def test_home_loads_with_empty_state(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "UniMarket")
        self.assertContains(response, "Ainda não há produtos publicados")

    def test_home_shows_active_products_and_hides_inactive(self):
        category = Category.objects.create(name="Livros")
        Product.objects.create(category=category, name="Cálculo I", price="350.00", stock=2)
        Product.objects.create(category=category, name="Oculto", price="10.00", is_active=False)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Cálculo I")
        self.assertContains(response, "350,00 MT")
        self.assertNotContains(response, "Oculto")

    def test_category_menu_is_rendered(self):
        Category.objects.create(name="Eletrónica")
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Eletrónica")
