from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from apps.chat.models import ChatSession, ChatMessage
from apps.chat.serializers import ChatSessionSerializer, ChatMessageSerializer
import uuid

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Bypass CSRF enforcement for public-facing chat endpoints."""
    def enforce_csrf(self, request):
        return

class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    
    @action(detail=False, methods=['post'])
    def init_session(self, request):
        session_token = str(uuid.uuid4())
        session = ChatSession.objects.create(session_token=session_token, language=request.data.get('language', 'en'))
        return Response({'session_token': session_token}, status=status.HTTP_201_CREATED)
        
    @method_decorator(ratelimit(key='ip', rate='20/m', block=True))
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        session_token = request.data.get('session_token')
        content = request.data.get('content')
        
        try:
            session = ChatSession.objects.get(session_token=session_token)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Invalid session'}, status=status.HTTP_404_NOT_FOUND)
            
        # Save user message
        user_message = ChatMessage.objects.create(session=session, sender='User', content=content)
        
        # Check for Yes/No continuations
        content_lower = content.strip().lower()
        if content_lower in ['no', 'nope', 'nah', 'not really']:
            # User wants to end the context
            session.current_context = None
            session.save()
            ai_response_text = "Thank you! Have a great day! Let me know if you have any other questions."
            ai_message = ChatMessage.objects.create(session=session, sender='AI', content=ai_response_text)
            return Response({
                'user_message': ChatMessageSerializer(user_message).data,
                'ai_response': ChatMessageSerializer(ai_message).data
            })
            
        # Generate AI response using single API call
        from services.ai_router import generate_response
        
        # Simple fast local context tracking (No API cost)
        content_lower = content.lower()
        topics = ['course', 'admission', 'fee', 'teacher', 'schedule', 'yoga', 'certif', 'contact']
        detected = None
        for t in topics:
            if t in content_lower:
                detected = t
                break
                
        if detected:
            session.current_context = detected
            session.save()
            
        ai_response_text = generate_response(prompt=content, current_context=session.current_context)
        
        # Save AI message
        ai_message = ChatMessage.objects.create(session=session, sender='AI', content=ai_response_text)
        
        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'ai_response': ChatMessageSerializer(ai_message).data
        })
