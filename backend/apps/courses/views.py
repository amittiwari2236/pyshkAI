from rest_framework import viewsets
from apps.courses.models import Course, FeeStructure
from apps.courses.serializers import CourseSerializer, FeeStructureSerializer
from rest_framework.permissions import AllowAny

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

class FeeStructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [AllowAny]
