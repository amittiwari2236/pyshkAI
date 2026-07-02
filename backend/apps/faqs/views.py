from rest_framework import viewsets
from apps.faqs.models import FAQ
from apps.faqs.serializers import FAQSerializer
from rest_framework.permissions import AllowAny

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
