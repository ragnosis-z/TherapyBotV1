"""Escalation Event Model"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class EscalationEvent(Base):
    """Escalation event model for tracking crisis situations"""

    __tablename__ = "escalation_events"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Escalation details
    escalation_type = Column(String(100), nullable=False)  # suicide, self_harm, severe_crisis, etc.
    severity = Column(Integer, default=0)  # 0-100 severity score
    trigger_message = Column(Text, nullable=False)  # The message that triggered escalation
    ai_response = Column(Text, nullable=False)  # Bot's response to the escalation
    
    # Follow-up
    is_resolved = Column(String(50), default="pending")  # pending, resolved, referred
    resolution_notes = Column(Text, nullable=True)
    referred_to = Column(String(255), nullable=True)  # Name of therapist/service referred to
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="escalation_events")

    def __repr__(self):
        return f"<EscalationEvent(id={self.id}, type={self.escalation_type}, severity={self.severity})>"
