from rest_framework import viewsets
from apps.teachers.models import Teacher
from apps.teachers.serializers import TeacherSerializer
from rest_framework.permissions import AllowAny

class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
