"""LLM Service for generating therapeutic responses"""

import logging
from typing import Optional, List, Dict, Tuple
from openai import OpenAI, APIError
import json

from app.config import settings
from app.utils.prompts import get_system_prompt

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM integration and response generation"""

    def __init__(self):
        """Initialize LLM service"""
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured. LLM responses will be template-based.")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_response(
        self,
        message: str,
        mode: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Tuple[str, int]:
        """
        Generate AI response using LLM

        Args:
            message: User's message
            mode: Therapeutic mode (witness, companion, gentle_guide, quiet_presence)
            conversation_history: Previous messages in conversation

        Returns:
            Tuple of (response_text, tokens_used)
        """
        if not self.client:
            # Fallback to template response if no API key
            return self._template_response(message, mode), 0

        try:
            system_prompt = get_system_prompt(mode)
            
            # Build messages list
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                timeout=settings.LLM_TIMEOUT,
            )
            
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(f"Generated response with {tokens_used} tokens using {settings.OPENAI_MODEL}")
            return response_text, tokens_used
            
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._template_response(message, mode), 0
        except Exception as e:
            logger.error(f"Unexpected error in LLM generation: {str(e)}")
            raise

    def _template_response(self, message: str, mode: str) -> str:
        """Generate template-based response when LLM is unavailable"""
        responses = {
            "witness": "I hear you. That sounds really important. I'm here to listen.",
            "companion": "You're not alone in this. I'm here with you. What matters most right now?",
            "gentle_guide": "Thank you for sharing that. What do you think might help right now?",
            "quiet_presence": "I'm here. Take the time you need.",
        }
        
        base = responses.get(mode, "I'm listening. Tell me more about what's on your mind.")
        return f"[{mode.upper()}] {base}"

    async def extract_emotional_content(self, message: str) -> Dict[str, any]:
        """
        Extract emotional content and sentiment from message

        Args:
            message: User's message

        Returns:
            Dictionary with emotional analysis
        """
        if not self.client:
            return {"sentiment": "neutral", "emotions": []}

        try:
            analysis_prompt = f"""Analyze the emotional content of this message and respond with JSON:
            Message: {message}
            
            Respond ONLY with valid JSON in this format:
            {{
                "sentiment": "positive|neutral|negative",
                "emotions": ["emotion1", "emotion2"],
                "emotional_intensity": 0-100
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=200,
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            logger.error(f"Error extracting emotional content: {str(e)}")
            return {"sentiment": "neutral", "emotions": [], "emotional_intensity": 0}
