from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count
from apps.courses.models import Course, FeeStructure
from apps.admissions.models import Admission
from apps.teachers.models import Teacher
from apps.schedules.models import Schedule
from apps.leads.models import Lead
from apps.faqs.models import FAQ
from apps.knowledge.models import Certification, YogaGuidance
from apps.chat.models import ChatMessage
from .serializers import (
    CourseSerializer, FeeStructureSerializer, AdmissionSerializer, 
    TeacherSerializer, ScheduleSerializer, LeadSerializer, 
    FAQSerializer, CertificationSerializer, YogaGuidanceSerializer
)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class CMSPermissionMixin:
    # Requires standard Django superuser or staff status
    authentication_classes = [CsrfExemptSessionAuthentication, JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

class CourseViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer

class FeeStructureViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all().order_by('-created_at')
    serializer_class = FeeStructureSerializer

class AdmissionViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Admission.objects.all().order_by('-created_at')
    serializer_class = AdmissionSerializer

class TeacherViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('-created_at')
    serializer_class = TeacherSerializer

class ScheduleViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('-created_at')
    serializer_class = ScheduleSerializer

class LeadViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer

class FAQViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = FAQ.objects.all().order_by('-created_at')
    serializer_class = FAQSerializer

class CertificationViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = Certification.objects.all().order_by('-created_at')
    serializer_class = CertificationSerializer

class YogaGuidanceViewSet(CMSPermissionMixin, viewsets.ModelViewSet):
    queryset = YogaGuidance.objects.all().order_by('-created_at')
    serializer_class = YogaGuidanceSerializer

@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_analytics(request):
    data = {
        'total_courses': Course.objects.count(),
        'total_faqs': FAQ.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_admissions': Admission.objects.count(),
        'total_leads': Lead.objects.count(),
        'total_chat_queries': ChatMessage.objects.filter(sender='User').count(),
    }
    return Response(data)

from rest_framework.views import APIView
from rest_framework import status
from apps.knowledge.models import UnifiedKnowledge
from .serializers import UnifiedKnowledgeSerializer

class UnifiedKnowledgeAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, module_name):
        try:
            knowledge = UnifiedKnowledge.objects.get(module_name=module_name)
            serializer = UnifiedKnowledgeSerializer(knowledge)
            return Response(serializer.data)
        except UnifiedKnowledge.DoesNotExist:
            return Response({'module_name': module_name, 'content': ''})

    def post(self, request, module_name):
        content = request.data.get('content', '')
        knowledge, created = UnifiedKnowledge.objects.update_or_create(
            module_name=module_name,
            defaults={'content': content}
        )
        serializer = UnifiedKnowledgeSerializer(knowledge)
        return Response(serializer.data, status=status.HTTP_200_OK)
