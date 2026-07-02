import re
import os
import google.generativeai as genai
from apps.knowledge.models import UnifiedKnowledge

def strip_html(text):
    if not text:
        return ""
    # Strip HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def semantic_extract(query, raw_text):
    """
    Uses Gemini to extract ONLY the facts relevant to the query from the raw_text.
    """
    if not raw_text.strip():
        return None
        
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return strip_html(raw_text) # Fallback to raw text if no API key
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are an intelligent knowledge extractor. 
Extract the exact information relevant to the user's query from the provided document.
If the document does not contain the answer, reply ONLY with "NOT_FOUND".
Do not hallucinate. Do not add conversational filler.

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

def extract_topic(query):
    """
    Uses Gemini to identify the primary module/topic from the user's natural language query.
    Expected outputs are one of the modules: courses, fees, admissions, teachers, schedules, yoga, certifications, faqs, contact.
    If none match, returns None.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return None
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are an intent classifier. Categorize the user's query into one of the following topics ONLY:
courses, fees, admissions, teachers, schedules, yoga, certifications, faqs, contact.

If the query doesn't match any of these topics, reply ONLY with "UNKNOWN".

User Query: "{query}"
Reply ONLY with the topic name or UNKNOWN. Do not add any punctuation or extra text.
"""
        response = model.generate_content(prompt)
        text = response.text.strip().lower()
        if text in ['courses', 'fees', 'admissions', 'teachers', 'schedules', 'yoga', 'certifications', 'faqs', 'contact']:
            return text
        return None
    except Exception as e:
        print(f"Topic extraction error: {e}")
        return None

def search_knowledge_base(query, session_topic=None):
    """
    1. Identify intent (which modules to search) using LLM.
    2. Retrieve UnifiedKnowledge content.
    3. Use semantic LLM extraction to pull exact facts.
    """
    # 1. Route the query to the correct UnifiedKnowledge modules using LLM
    requested_modules = set()
    
    extracted_module = extract_topic(query)
    
    if extracted_module:
        requested_modules.add(extracted_module)
    elif session_topic and session_topic in ['courses', 'fees', 'admissions', 'teachers', 'schedules', 'yoga', 'certifications', 'faqs', 'contact']:
        requested_modules.add(session_topic)
    else:
        # Fallback to general modules if no specific intent is found
        requested_modules.update(['courses', 'fees', 'admissions', 'teachers', 'schedules', 'yoga', 'certifications', 'faqs', 'contact'])
        
    # 2. Fetch the raw unstructured text from the DB
    combined_raw_text = ""
    for mod in requested_modules:
        try:
            doc = UnifiedKnowledge.objects.get(module_name=mod)
            if doc.content.strip():
                combined_raw_text += f"\n--- {mod.upper()} ---\n{doc.content}\n"
        except UnifiedKnowledge.DoesNotExist:
            continue
            
    if not combined_raw_text.strip():
        return None
        
    # 3. Semantic Extraction
    extracted_facts = semantic_extract(query, combined_raw_text)
    
    return extracted_facts
