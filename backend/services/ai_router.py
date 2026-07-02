import logging
from services.gemini_service import generate_ai_response as gemini_generate
from services.openai_service import generate_ai_response as openai_generate

logger = logging.getLogger(__name__)

def generate_response(prompt, current_context=None):
    """
    Unified AI router. Prioritizes Gemini.
    Passes the chunked DB context directly to Gemini to save API calls.
    Falls back to OpenAI if Gemini fails due to rate limits.
    """
    from services.search_service import search_knowledge_base
    
    # 1. Search the database for the user's query and get top chunks
    db_context = search_knowledge_base(prompt)
    
    # 2. If nothing is found in the database, refuse to answer WITHOUT calling the AI!
    if not db_context:
        logger.info("No DB match found for query. Refusing to answer to prevent hallucination and save quota.")
        return "Sorry, I couldn't find this information in the PYSHK Knowledge Base. Please contact our support team for assistance."
        
    try:
        logger.info("Attempting to format response using Google Gemini.")
        # Pass the prompt, the DB chunks, and the context
        return gemini_generate(prompt, db_context, current_context)
    except Exception as gemini_err:
        logger.warning(f"Gemini generation failed: {gemini_err}. Falling back to OpenAI.")
        
    try:
        logger.info("Attempting to generate response using OpenAI (Fallback).")
        return openai_generate(prompt, db_context, current_context)
    except Exception as openai_err:
        logger.error(f"OpenAI generation failed: {openai_err}. Both providers unavailable.")
        return "Sorry, the AI service is temporarily unavailable. Please try again in a few moments."

