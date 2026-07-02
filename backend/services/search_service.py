import re
import os
import google.generativeai as genai
from apps.knowledge.models import CentralKnowledge

def strip_html(text):
    if not text:
        return ""
    # Strip HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def semantic_extract(query, raw_text, current_context=None):
    """
    Uses Gemini to extract ONLY the facts relevant to the query from the raw_text.
    It inherently handles semantic matching and intent detection.
    """
    if not raw_text.strip():
        return None
        
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return strip_html(raw_text) # Fallback to raw text if no API key
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        context_prompt = f"Previous conversation context: {current_context}\n" if current_context else ""
        
        prompt = f"""
You are an intelligent knowledge extractor and intent detector.
Extract the exact information relevant to the user's query from the provided document.
Use semantic matching and synonym detection (e.g., 'faculty' means 'teachers', 'cost' means 'fees').
If the document does not contain the answer, reply ONLY with "NOT_FOUND".
Do not hallucinate. Do not add conversational filler.

{context_prompt}
User Query: "{query}"

Document Text:
{strip_html(raw_text)}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text == "NOT_FOUND" or "NOT_FOUND" in text:
            return None
        return text
    except Exception as e:
        print(f"Extraction error: {e}")
        return strip_html(raw_text) # Fallback

def get_new_context(query, current_context=None):
    """
    Summarizes the current context of the conversation using the latest query.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return query[:100]
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
Summarize the main topic of this user's query into a short phrase (max 3-5 words) to maintain conversation context.
Previous context: {current_context or 'None'}
User query: {query}
Reply ONLY with the short phrase. No punctuation.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return query[:100]

def search_knowledge_base(query, session_context=None):
    """
    Retrieves the entire Central Knowledge base and semantically extracts the answer.
    """
    try:
        central_kb = CentralKnowledge.objects.first()
        if not central_kb or not central_kb.content.strip():
            return None
            
        combined_raw_text = central_kb.content
    except Exception as e:
        print(f"Error fetching CentralKnowledge: {e}")
        return None
        
    # Semantic Extraction
    extracted_facts = semantic_extract(query, combined_raw_text, current_context=session_context)
    
    return extracted_facts
