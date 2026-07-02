from django.db import models
from core.models import BaseModel
from apps.courses.models import Course
from apps.teachers.models import Teacher

class Schedule(BaseModel):
    course = models.ForeignKey(Course, related_name='schedules', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='schedules', on_delete=models.SET_NULL, null=True, blank=True)
    batch_type = models.CharField(max_length=50, choices=(('Daily', 'Daily'), ('Weekend', 'Weekend')))
    class_mode = models.CharField(max_length=50, choices=(('Online', 'Online'), ('Offline', 'Offline')))
    timings = models.CharField(max_length=255)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.name} - {self.batch_type} ({self.class_mode})"
