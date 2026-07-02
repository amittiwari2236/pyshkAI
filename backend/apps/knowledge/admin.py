from django.contrib import admin
from apps.knowledge.models import KnowledgeDocument
from services.document_parser import process_document

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'is_active', 'created_at')
    list_filter = ('document_type', 'is_active')
    search_fields = ('title', 'extracted_text')
    actions = ['extract_text']
    
    @admin.action(description='Extract text from selected documents')
    def extract_text(self, request, queryset):
        success_count = 0
        for doc in queryset:
            if process_document(doc):
                success_count += 1
        self.message_user(request, f'Successfully extracted text for {success_count} documents.')
