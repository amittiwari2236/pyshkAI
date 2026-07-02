from django.contrib import admin
from apps.chat.models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_token', 'user', 'language', 'created_at')
    inlines = [ChatMessageInline]
    search_fields = ('session_token',)
