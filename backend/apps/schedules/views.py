from rest_framework import viewsets
from apps.schedules.models import Schedule
from apps.schedules.serializers import ScheduleSerializer
from rest_framework.permissions import AllowAny

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]
