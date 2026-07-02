import os
from apps.knowledge.models import CentralKnowledge

def search_knowledge_base():
    """
    Retrieves the entire Central Knowledge base raw text.
    Semantic extraction is now handled directly by the conversational AI to save API quota.
    """
    try:
        central_kb = CentralKnowledge.objects.first()
        if not central_kb or not central_kb.content.strip():
            return None
            
        return central_kb.content
    except Exception as e:
        print(f"Error fetching CentralKnowledge: {e}")
        return None
