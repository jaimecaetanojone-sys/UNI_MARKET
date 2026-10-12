from django.conf import settings

from apps.products.models import Category


def site_settings(request):
    """Disponibiliza o nome do site, a moeda e as categorias a todos os templates."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "CURRENCY_SYMBOL": settings.CURRENCY_SYMBOL,
        "nav_categories": Category.objects.filter(is_active=True).order_by("name"),
    }
