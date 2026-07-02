import os
from openai import OpenAI
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
"""

def get_openai_client():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        raise ValueError("OPENAI_API_KEY is missing or invalid.")
    return OpenAI(api_key=api_key)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def generate_ai_response(prompt, db_context, current_context=None):
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
    ]
    
    context_str = f"Previous conversation context: {current_context}\n\n" if current_context else ""
    full_prompt = f"{context_str}Knowledge Base Context:\n{db_context}\n\nUser Question:\n{prompt}"
        
    messages.append({"role": "user", "content": full_prompt})
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            timeout=15.0
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        raise e
