from django.conf import settings

from .models import ContactInfo

def contact_info(request):
    return {
        'contact_info': ContactInfo.objects.first(),
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }