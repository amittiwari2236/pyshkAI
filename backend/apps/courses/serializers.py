from rest_framework import serializers
from apps.courses.models import Course, FeeStructure

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    fees = FeeStructureSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
