from django.contrib import admin
from django.apps import apps
from django.urls import path, include

# Auto-register all models in the admin panel
for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import views
from apps.users.views import UserViewSet
from apps.chat.views import ChatViewSet
from apps.knowledge.views import KnowledgeDocumentViewSet
from apps.courses.views import CourseViewSet, FeeStructureViewSet
from apps.admissions.views import AdmissionViewSet
from apps.teachers.views import TeacherViewSet
from apps.schedules.views import ScheduleViewSet
from apps.leads.views import LeadViewSet
from apps.faqs.views import FAQViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'knowledge', KnowledgeDocumentViewSet, basename='knowledge')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'fees', FeeStructureViewSet, basename='fees')
router.register(r'admissions', AdmissionViewSet, basename='admissions')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'schedules', ScheduleViewSet, basename='schedules')
router.register(r'leads', LeadViewSet, basename='leads')
router.register(r'faqs', FAQViewSet, basename='faqs')

cms_router = DefaultRouter()
from apps.cms.views import (
    UnifiedKnowledgeAPIView,
    CourseViewSet as CMSCourseViewSet,
    FeeStructureViewSet as CMSFeeStructureViewSet,
    AdmissionViewSet as CMSAdmissionViewSet,
    TeacherViewSet as CMSTeacherViewSet,
    ScheduleViewSet as CMSScheduleViewSet,
    LeadViewSet as CMSLeadViewSet,
    FAQViewSet as CMSFAQViewSet,
    CertificationViewSet as CMSCertificationViewSet,
    YogaGuidanceViewSet as CMSYogaGuidanceViewSet,
    dashboard_analytics
)
cms_router.register(r'courses', CMSCourseViewSet, basename='cms_courses')
cms_router.register(r'fees', CMSFeeStructureViewSet, basename='cms_fees')
cms_router.register(r'admissions', CMSAdmissionViewSet, basename='cms_admissions')
cms_router.register(r'teachers', CMSTeacherViewSet, basename='cms_teachers')
cms_router.register(r'schedules', CMSScheduleViewSet, basename='cms_schedules')
cms_router.register(r'leads', CMSLeadViewSet, basename='cms_leads')
cms_router.register(r'faqs', CMSFAQViewSet, basename='cms_faqs')
cms_router.register(r'certifications', CMSCertificationViewSet, basename='cms_certifications')
cms_router.register(r'yoga', CMSYogaGuidanceViewSet, basename='cms_yoga')

from django.views.generic import TemplateView
from django.views.static import serve
import os

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': os.path.join(settings.BASE_DIR, '..', 'frontend')}),
    path('admin/', admin.site.urls),
    
    # JWT Auth Endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Core APIs
    path('api/', include(router.urls)),
    
    # CMS APIs
    path('api/cms/dashboard/', dashboard_analytics, name='cms_dashboard'),
    path('api/cms/', include(cms_router.urls)),
    path('api/cms/unified-knowledge/<str:module_name>/', UnifiedKnowledgeAPIView.as_view(), name='unified_knowledge'),
    
    # CMS Frontend App
    path('cms/', TemplateView.as_view(template_name='admin/index.html'), name='cms_frontend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
