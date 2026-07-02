from rest_framework import viewsets
from apps.knowledge.models import KnowledgeDocument
from apps.knowledge.serializers import KnowledgeDocumentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
