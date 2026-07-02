from rest_framework import viewsets, mixins
from apps.leads.models import Lead
from apps.leads.serializers import LeadSerializer
from rest_framework.permissions import AllowAny

class LeadViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        from rest_framework.permissions import IsAdminUser
        return [IsAdminUser()]
