from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Product


class ProductListView(ListView):
    """Lista pública com pesquisa por texto, categoria e intervalo de preço."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category")
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("categoria", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category__slug=category, category__is_active=True)
        for param, lookup in (("preco_min", "price__gte"), ("preco_max", "price__lte")):
            raw = self.request.GET.get(param, "").strip()
            if raw:
                try:
                    qs = qs.filter(**{lookup: raw})
                except (ValueError, ArithmeticError):
                    pass  # valor inválido: ignora o filtro em vez de gerar erro
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["selected_category"] = self.request.GET.get("categoria", "").strip()
        context["preco_min"] = self.request.GET.get("preco_min", "")
        context["preco_max"] = self.request.GET.get("preco_max", "")
        querydict = self.request.GET.copy()
        querydict.pop("page", None)
        context["querystring"] = querydict.urlencode()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")
