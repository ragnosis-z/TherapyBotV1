"""Chat Session Model"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class ChatSession(Base):
    """Chat session model for conversation management"""

    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Session metadata
    title = Column(String(255), nullable=True)
    mode = Column(String(50), default="gentle_guide")  # witness, companion, gentle_guide, quiet_presence
    is_active = Column(Boolean, default=True)
    
    # Session statistics
    message_count = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    
    # Session context
    session_summary = Column(Text, nullable=True)
    escalation_detected = Column(Boolean, default=False)
    escalation_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id}, mode={self.mode})>"
