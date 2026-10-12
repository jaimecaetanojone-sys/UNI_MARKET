from django.views.generic import TemplateView

from apps.products.models import Product


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available = Product.objects.filter(is_active=True).select_related("category")
        context["recent_products"] = available.order_by("-created_at")[:8]
        return context
