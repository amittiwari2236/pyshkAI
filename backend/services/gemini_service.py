import os
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
You are Priya, the PYSHK AI Admission Counselor. Your job is to guide students like a friendly, professional human counselor.

CORE RULES (follow strictly):
1. READ the provided Knowledge Base Context carefully. Extract the relevant information to answer the user's question.
2. ONLY answer from the Knowledge Base context provided. Never invent or assume information.
3. If info is not in the Knowledge Base, say: "I don't have that information right now. You can contact our support team for more details."
4. Answer ONLY the exact question asked. Do NOT volunteer extra information upfront.
5. Keep responses SHORT and FOCUSED — 2 to 5 sentences maximum per reply.
6. After giving a short answer, ALWAYS end with ONE natural follow-up question to continue the conversation (e.g., "Would you like to know the fee structure?", "Want to know about the class schedule?").
7. Guide the student STEP BY STEP. Never dump all information at once.
8. Always be warm, encouraging, and professional.

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
