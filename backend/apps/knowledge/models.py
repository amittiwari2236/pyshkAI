from django.db import models
from core.models import BaseModel

class KnowledgeDocument(BaseModel):
    DOC_TYPES = (
        ('PDF', 'PDF'),
        ('Word', 'Word'),
        ('Excel', 'Excel'),
        ('Text', 'Text'),
    )
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=10, choices=DOC_TYPES)
    file = models.FileField(upload_to='knowledge_docs/')
    extracted_text = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Certification(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class YogaGuidance(BaseModel):
    topic = models.CharField(max_length=255)
    guidelines = models.TextField()
    benefits = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='yoga_guidance/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.topic

class UnifiedKnowledge(BaseModel):
    """
    Stores the unified, unstructured rich text content for a specific CMS module.
    """
    module_name = models.CharField(max_length=100, unique=True, db_index=True)
    content = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"Unified Knowledge: {self.module_name}"
