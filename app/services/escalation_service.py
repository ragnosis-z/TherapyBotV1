"""Escalation Service for crisis detection and response"""

import logging
from typing import Optional, Tuple
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from app.models import EscalationEvent, ChatSession
from app.config import settings
from app.utils.safety import get_crisis_response, detect_crisis_keywords

logger = logging.getLogger(__name__)


class EscalationService:
    """Service for handling escalation detection and crisis response"""

    # Crisis keywords and phrases
    CRISIS_KEYWORDS = {
        "suicide": ["want to die", "kill myself", "no point", "not worth living", "end it"],
        "self_harm": ["hurt myself", "cut myself", "self-harm", "self harm"],
        "severe_distress": ["can't bear", "unbearable", "at breaking point", "complete breakdown"],
    }

    CRISIS_HOTLINES = {
        "us": {
            "name": "988 Suicide & Crisis Lifeline",
            "phone": "988",
            "url": "https://988lifeline.org/chat",
        },
        "crisis_text": {
            "name": "Crisis Text Line",
            "phone": "Text HOME to 741741",
            "url": "https://www.crisistextline.org/",
        },
    }

    def __init__(self, db: Session):
        """Initialize escalation service"""
        self.db = db

    async def check_for_escalation(
        self,
        message: str,
        session_id: str,
        user_id: str,
    ) -> Tuple[bool, Optional[str], str]:
        """
        Check if message indicates escalation needed

        Args:
            message: User's message to analyze
            session_id: Current chat session ID
            user_id: User ID

        Returns:
            Tuple of (is_escalation, escalation_type, ai_response)
        """
        if not settings.ENABLE_SAFETY_CHECK:
            return False, None, ""

        message_lower = message.lower()
        escalation_type = None

        # Check for crisis keywords
        for crisis_type, keywords in self.CRISIS_KEYWORDS.items():
            if any(keyword in message_lower for keyword in keywords):
                escalation_type = crisis_type
                break

        if not escalation_type:
            return False, None, ""

        # Generate crisis response
        ai_response = get_crisis_response(escalation_type)

        # Log escalation event
        await self._log_escalation_event(user_id, escalation_type, message, ai_response)

        # Update session with escalation flag
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.escalation_detected = True
            session.escalation_reason = escalation_type
            self.db.commit()

        logger.warning(
            f"Escalation detected: type={escalation_type}, user_id={user_id}, session_id={session_id}"
        )

        return True, escalation_type, ai_response

    async def _log_escalation_event(
        self,
        user_id: str,
        escalation_type: str,
        trigger_message: str,
        ai_response: str,
    ) -> None:
        """
        Log an escalation event to database

        Args:
            user_id: User ID
            escalation_type: Type of escalation
            trigger_message: Message that triggered escalation
            ai_response: Bot's response
        """
        try:
            event = EscalationEvent(
                id=str(uuid.uuid4()),
                user_id=user_id,
                escalation_type=escalation_type,
                severity=self._calculate_severity(escalation_type),
                trigger_message=trigger_message,
                ai_response=ai_response,
            )
            
            self.db.add(event)
            self.db.commit()
            logger.info(f"Escalation event logged: {event.id}")
            
        except Exception as e:
            logger.error(f"Error logging escalation event: {str(e)}")
            self.db.rollback()

    def _calculate_severity(self, escalation_type: str) -> int:
        """
        Calculate severity score for escalation type

        Args:
            escalation_type: Type of escalation

        Returns:
            Severity score 0-100
        """
        severity_map = {
            "suicide": 100,
            "self_harm": 80,
            "severe_distress": 60,
        }
        return severity_map.get(escalation_type, 50)

    def get_crisis_hotlines(self) -> dict:
        """Return crisis hotline information"""
        return self.CRISIS_HOTLINES

    async def update_escalation_resolution(
        self,
        escalation_id: str,
        resolution_status: str,
        notes: Optional[str] = None,
        referred_to: Optional[str] = None,
    ) -> None:
        """
        Update escalation event with resolution information

        Args:
            escalation_id: ID of escalation event
            resolution_status: Resolution status (pending, resolved, referred)
            notes: Resolution notes
            referred_to: Name of service/therapist referred to
        """
        try:
            event = self.db.query(EscalationEvent).filter(
                EscalationEvent.id == escalation_id
            ).first()
            
            if event:
                event.is_resolved = resolution_status
                event.resolution_notes = notes
                event.referred_to = referred_to
                event.resolved_at = datetime.utcnow()
                self.db.commit()
                logger.info(f"Escalation {escalation_id} marked as {resolution_status}")
                
        except Exception as e:
            logger.error(f"Error updating escalation: {str(e)}")
            self.db.rollback()
