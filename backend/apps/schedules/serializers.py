from rest_framework import serializers
from apps.schedules.models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    
    class Meta:
        model = Schedule
        fields = '__all__'
