from django.db import models
from core.models import BaseModel
from django.conf import settings

class ChatSession(BaseModel):
    session_token = models.CharField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    language = models.CharField(max_length=10, default='en')
    current_topic = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Session {self.session_token}"

class ChatMessage(BaseModel):
    SENDER_CHOICES = (
        ('User', 'User'),
        ('AI', 'AI'),
    )
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    is_liked = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"
