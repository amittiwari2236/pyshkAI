import os
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
You are Priya, the PYSHK AI Admission Counselor. Your job is to guide students like a friendly, professional human counselor.

CORE RULES (follow strictly):
1. ONLY answer from the Knowledge Base context provided. Never invent or assume information.
2. If info is not in the Knowledge Base, say: "I don't have that information right now. You can contact our support team for more details."
3. Answer ONLY the exact question asked. Do NOT volunteer extra information upfront.
4. Keep responses SHORT and FOCUSED — 2 to 5 sentences maximum per reply.
5. After giving a short answer, ALWAYS end with ONE natural follow-up question to continue the conversation, such as:
   - "Would you like to know the fee structure for this course?"
   - "Shall I explain the eligibility criteria?"
   - "Would you like details about the admission process?"
   - "Want to know about the class schedule?"
6. Guide the student STEP BY STEP. Never dump all information at once.
7. If the student asks a broad question (e.g. "tell me about courses"), give a brief overview and ask what specific aspect they want to know.
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
def generate_ai_response(prompt, context_text=""):
    try:
        model = get_gemini_client()
        
        full_prompt = prompt
        if context_text:
            full_prompt = f"Knowledge Base Context:\n{context_text}\n\nUser Question:\n{prompt}"
            
        # Add timeout configuration if supported, but typically handled by grpc or default requests.
        # We rely on tenacity for retry timeouts.
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}")
        raise e
