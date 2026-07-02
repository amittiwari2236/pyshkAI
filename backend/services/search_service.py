import os
import re
from apps.knowledge.models import CentralKnowledge

# Common English stop words
STOP_WORDS = set(['what', 'are', 'the', 'is', 'in', 'of', 'and', 'to', 'a', 'for', 'on', 'with', 'as', 'by', 'an', 'this', 'that', 'how', 'do', 'i', 'can', 'you', 'tell', 'me', 'about', 'does'])

# Synonyms for better matching
SYNONYMS = {
    'fee': ['cost', 'price', 'charge', 'amount', 'fees', 'tuition'],
    'teacher': ['faculty', 'instructor', 'trainer', 'staff', 'teachers', 'professor'],
    'course': ['program', 'class', 'training', 'courses', 'certification', 'yog'],
    'schedule': ['timing', 'time', 'timetable', 'batch', 'schedules', 'dates'],
    'admission': ['enroll', 'enrollment', 'register', 'join', 'apply', 'admissions'],
}

def strip_html(text):
    if not text:
        return ""
    # Replace block tags with newline for better chunking
    text = re.sub(r'</p>|<br\s*/?>|</h1>|</h2>|</h3>|</li>', '\n', text, flags=re.IGNORECASE)
    # Strip all remaining HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, ' ', text)
    # Normalize whitespace
    return re.sub(r'[ \t]+', ' ', text)

def tokenize(text):
    words = re.findall(r'\b\w+\b', text.lower())
    tokens = set()
    for w in words:
        if w not in STOP_WORDS:
            tokens.add(w)
            # Add synonyms
            for key, syn_list in SYNONYMS.items():
                if w == key or w in syn_list:
                    tokens.add(key)
                    for s in syn_list:
                        tokens.add(s)
    return tokens

def search_knowledge_base(query):
    """
    Retrieves and ranks the most relevant chunks from the Central Knowledge Base.
    Returns the top paragraphs or None if no match is found.
    """
    try:
        central_kb = CentralKnowledge.objects.first()
        if not central_kb or not central_kb.content.strip():
            return None
            
        raw_text = central_kb.content
    except Exception as e:
        print(f"Error fetching CentralKnowledge: {e}")
        return None

    clean_text = strip_html(raw_text)
    # Split into chunks (paragraphs) by newlines
    chunks = [chunk.strip() for chunk in clean_text.split('\n') if len(chunk.strip()) > 20]
    
    query_tokens = tokenize(query)
    
    if not query_tokens:
        return None # Too short or only stop words

    scored_chunks = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0
        for token in query_tokens:
            if token in chunk_lower:
                # Add weight based on word frequency in chunk
                score += chunk_lower.count(token)
                
        if score > 0:
            scored_chunks.append((score, chunk))
            
    if not scored_chunks:
        return None
        
    # Sort by score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Extract top 4 most relevant chunks
    top_chunks = [chunk for score, chunk in scored_chunks[:4]]
    
    return "\n\n".join(top_chunks)
