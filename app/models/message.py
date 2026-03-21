"""Message Model"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Message(Base):
    """Message model for conversation history"""

    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, index=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False, index=True)
    
    # Message content
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    
    # Message metadata
    tokens_used = Column(Integer, default=0)
    safety_flagged = Column(String(255), nullable=True)  # Reason if flagged
    escalation_score = Column(Integer, default=0)  # 0-100 escalation severity
    
    # Model info
    model_used = Column(String(255), nullable=True)  # Which LLM model generated this
    temperature = Column(String(10), nullable=True)  # Temperature used for generation
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, tokens={self.tokens_used})>"
