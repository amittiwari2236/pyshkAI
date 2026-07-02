from django.db import models
from core.models import BaseModel

class Teacher(BaseModel):
    name = models.CharField(max_length=255)
    experience_years = models.IntegerField(default=0)
    qualifications = models.TextField()
    specialization = models.CharField(max_length=255)
    profile_summary = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='teachers/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
