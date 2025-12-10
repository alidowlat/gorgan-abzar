from core.models import Settings


def site_defaults(request):
    return {
        "SITE_TITLE": "گرگان ابزار",
    }

def site_settings(request):
    settings = Settings.objects.filter(is_main=True).first()
    return {
        "SITE_SETTINGS": settings,
    }