from rest_framework import viewsets
from apps.admissions.models import Admission
from apps.admissions.serializers import AdmissionSerializer
from rest_framework.permissions import AllowAny

class AdmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [AllowAny]
