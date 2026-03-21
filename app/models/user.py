"""User Model"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    """User model for authentication and profile management"""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Mental health profile
    primary_concerns = Column(Text, nullable=True)  # JSON string of primary concerns
    preferred_mode = Column(String(50), default="gentle_guide")  # witness, companion, gentle_guide, quiet_presence
    support_contact_name = Column(String(255), nullable=True)
    support_contact_phone = Column(String(20), nullable=True)
    
    # Clinical data
    initial_assessment = Column(Text, nullable=True)  # Initial mental health assessment
    consent_to_ai_therapy = Column(Boolean, default=False)
    emergency_contact = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    escalation_events = relationship("EscalationEvent", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
