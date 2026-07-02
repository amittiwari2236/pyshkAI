import os
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
You are Priya, the PYSHK AI Admission Counselor. Your job is to format the provided retrieved Knowledge Base chunks into a friendly, professional response.

CORE RULES (follow strictly):
1. You are a FORMATTER. The user's question has already been searched against the database, and the relevant paragraphs are provided to you.
2. ONLY answer using the exact facts provided in the Knowledge Base Context. Never invent, assume, or hallucinate information.
3. Answer ONLY the exact question asked. Do NOT volunteer extra information upfront.
4. Keep responses SHORT and FOCUSED — 2 to 5 sentences maximum per reply.
5. Organize the retrieved content into headings, bullet points, or tables if it improves readability.
6. After giving your formatted answer, ALWAYS end with ONE natural follow-up question to continue the conversation.
7. Always be warm, encouraging, and professional.

FORMATTING:
- Use **bold** for important terms.
- Use bullet points only when listing 3 or more items.
- Keep responses readable on a mobile screen.
- Do NOT use large headings (##) for short answers.
"""

def get_gemini_client():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        raise ValueError("GEMINI_API_KEY is missing or invalid.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_INSTRUCTION)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def generate_ai_response(prompt, db_context, current_context=None):
    try:
        model = get_gemini_client()
        
        context_str = f"Previous conversation context: {current_context}\n\n" if current_context else ""
        
        full_prompt = f"""{context_str}Knowledge Base Context:
{db_context}

User Question:
{prompt}"""
            
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}")
        raise e
