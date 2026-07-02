from rest_framework import serializers
from apps.courses.models import Course, FeeStructure
from apps.admissions.models import Admission
from apps.teachers.models import Teacher
from apps.schedules.models import Schedule
from apps.leads.models import Lead
from apps.faqs.models import FAQ
from apps.knowledge.models import Certification, YogaGuidance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class YogaGuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = YogaGuidance
        fields = '__all__'

from apps.knowledge.models import CentralKnowledge

class CentralKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentralKnowledge
        fields = '__all__'
