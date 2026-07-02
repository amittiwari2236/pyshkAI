from django.db import models
from core.models import BaseModel
from apps.chat.models import ChatSession

class VoiceLog(BaseModel):
    session = models.ForeignKey(ChatSession, related_name='voice_logs', on_delete=models.CASCADE)
    audio_file_path = models.CharField(max_length=500)
    transcribed_text = models.TextField()
    duration_seconds = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Voice Log for Session {self.session.session_token}"
