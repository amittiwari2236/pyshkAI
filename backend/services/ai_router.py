import logging
from services.gemini_service import generate_ai_response as gemini_generate
from services.openai_service import generate_ai_response as openai_generate

logger = logging.getLogger(__name__)

def generate_response(prompt, context_text="", current_context=None):
    """
    Unified AI router. Prioritizes Gemini.
    Falls back to OpenAI on failure.
    Returns a standard friendly message if both fail.
    """
    # --- STRICT DB GROUNDING LOGIC ---
    from services.search_service import search_knowledge_base
    
    # 1. Search the database for the user's query
    db_context = search_knowledge_base(prompt, session_context=current_context)
    
    # 2. If nothing is found in the database, refuse to answer
    if not db_context:
        logger.info("No DB match found for query. Refusing to answer to prevent hallucination.")
        return "Sorry, I couldn't find this information in the PYSHK Knowledge Base. Please contact our support team for assistance."
        
    # 3. If found, combine DB context with any passed context
    final_context = db_context
    if context_text:
        final_context = f"{context_text}\n\n{db_context}"
    # ---------------------------------

    # Instruct the AI to ask a follow-up if we have a current topic
    modified_prompt = prompt
    if current_topic:
        modified_prompt = f"{prompt}\n\n[Instruction: End your response by asking: 'Would you like more details on this topic or have another question about {current_topic}?']"

    try:
        logger.info("Attempting to generate response using Google Gemini (Primary).")
        return gemini_generate(modified_prompt, context_text=final_context)
    except Exception as gemini_err:
        logger.warning(f"Gemini generation failed: {gemini_err}. Falling back to OpenAI.")
        
    try:
        logger.info("Attempting to generate response using OpenAI (Fallback).")
        return openai_generate(modified_prompt, context_text=final_context)
    except Exception as openai_err:
        logger.error(f"OpenAI generation failed: {openai_err}. Both providers unavailable.")
        
    return "Sorry, the AI service is temporarily unavailable. Please try again in a few moments."
