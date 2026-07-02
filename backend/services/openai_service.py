import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
You are the PYSHK AI Smart Assistant. You answer student queries related to admissions, courses, fees, teachers, schedules, and yoga.
Use the provided Knowledge Base context to answer the user's question accurately.
If the answer is found in the Knowledge Base context, prioritize it.
If the answer is NOT in the Knowledge Base context, use your best judgment to provide a helpful response, but clearly mention that your response is AI-generated and not from the official Knowledge Base.
Do NOT hallucinate information about courses or fees.

FORMATTING REQUIREMENTS:
- Format your response beautifully using Markdown.
- Use proper headings (## or ###) and subheadings to structure your response.
- Use bullet points or numbered lists for multiple items or steps.
- Highlight important keywords using **bold text**.
- Keep paragraphs short (2-4 lines).
- Display tables for structured information like course fees, schedules, or comparisons.
- Ensure the final response looks polished, professional, and easy to read.
"""

def get_openai_client():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        raise ValueError("OPENAI_API_KEY is missing or invalid.")
    return OpenAI(api_key=api_key)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def generate_ai_response(prompt, context_text=""):
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
    ]
    
    if context_text:
        messages.append({"role": "system", "content": f"Knowledge Base Context:\n{context_text}"})
        
    messages.append({"role": "user", "content": prompt})
    
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
