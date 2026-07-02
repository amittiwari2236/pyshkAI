from django.db import models
from core.models import BaseModel
from apps.courses.models import Course

class Admission(BaseModel):
    course = models.ForeignKey(Course, related_name='admissions', on_delete=models.CASCADE)
    process_details = models.TextField()
    documents_required = models.TextField()
    eligibility_criteria = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Admission for {self.course.name}"
