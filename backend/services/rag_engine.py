from apps.knowledge.models import KnowledgeDocument
from apps.faqs.models import FAQ

def retrieve_context(query):
    """
    A simple baseline RAG engine using Django ORM text search.
    In a full production RAG, this would be replaced with Vector Embeddings (Pinecone/pgvector).
    """
    context = ""
    
    # 1. Check FAQs first (Exact or partial match)
    # Using simple icontains for baseline.
    faqs = FAQ.objects.filter(is_active=True, question__icontains=query)
    if faqs.exists():
        context += "FAQ Context:\\n"
        for faq in faqs[:3]:
            context += f"Q: {faq.question}\\nA: {faq.answer}\\n\\n"
            
    # 2. Search extracted text in Knowledge Documents
    docs = KnowledgeDocument.objects.filter(is_active=True, extracted_text__icontains=query)
    if docs.exists():
        context += "Document Context:\\n"
        for doc in docs[:2]:
            # Simple snippet extraction (this is basic; vector search would be superior)
            text = doc.extracted_text
            idx = text.lower().find(query.lower())
            start = max(0, idx - 200)
            end = min(len(text), idx + 500)
            context += text[start:end] + "...\\n\\n"
            
    return context
