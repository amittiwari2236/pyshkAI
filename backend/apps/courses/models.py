from django.db import models
from core.models import BaseModel

class Course(BaseModel):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    eligibility = models.TextField()
    details = models.TextField()
    benefits = models.TextField()
    syllabus = models.TextField()
    career_opportunities = models.TextField()
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    brochure = models.FileField(upload_to='courses/brochures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class FeeStructure(BaseModel):
    course = models.OneToOneField(Course, related_name='fees', on_delete=models.CASCADE)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    installment_options = models.TextField(blank=True, null=True)
    discount_info = models.TextField(blank=True, null=True)
    scholarships = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Fees for {self.course.name}"
