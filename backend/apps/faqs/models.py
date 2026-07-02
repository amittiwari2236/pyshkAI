from django.db import models
from core.models import BaseModel

class FAQ(BaseModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
