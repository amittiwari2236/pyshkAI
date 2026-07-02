from rest_framework import serializers
from apps.admissions.models import Admission

class AdmissionSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Admission
        fields = '__all__'
