from django.db import models
from core.models import BaseModel
from apps.courses.models import Course

class Lead(BaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    course_interest = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100, blank=True, null=True)
    preferred_language = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
