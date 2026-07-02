import logging
from services.gemini_service import generate_ai_response as gemini_generate

logger = logging.getLogger(__name__)

def generate_response(prompt, current_context=None):
    """
    Unified AI router. Prioritizes Gemini.
    Passes the raw DB context directly to Gemini to save API calls.
    """
    from services.search_service import search_knowledge_base
    
    # 1. Get raw database text
    db_context = search_knowledge_base()
    
    # 2. If nothing is found in the database, refuse to answer
    if not db_context:
        logger.info("No DB match found for query. Refusing to answer to prevent hallucination.")
        return "Sorry, I couldn't find this information in the PYSHK Knowledge Base. Please contact our support team for assistance."
        
    try:
        logger.info("Attempting to generate response using Google Gemini.")
        # Pass the prompt, the DB text, and the context
        return gemini_generate(prompt, db_context, current_context)
    except Exception as gemini_err:
        logger.error(f"Gemini generation failed: {gemini_err}")
        return "Sorry, the AI service is temporarily unavailable. Please try again in a few moments."

