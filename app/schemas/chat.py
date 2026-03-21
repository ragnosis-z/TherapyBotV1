"""Chat Request/Response Schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ModeEnum(str, Enum):
    """Therapeutic conversation modes"""
    witness = "witness"
    companion = "companion"
    gentle_guide = "gentle_guide"
    quiet_presence = "quiet_presence"


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    mode: Optional[ModeEnum] = Field(default="gentle_guide", description="Therapeutic mode")
    session_id: Optional[str] = Field(None, description="Existing session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "I'm feeling really overwhelmed today",
                "mode": "companion",
                "session_id": None
            }
        }


class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str
    mode: ModeEnum
    session_id: str
    message_id: str
    escalation_detected: bool = False
    escalation_type: Optional[str] = None
    tokens_used: int = 0
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I can sense that things feel heavy right now. That's real.",
                "mode": "witness",
                "session_id": "sess_123",
                "message_id": "msg_456",
                "escalation_detected": False,
                "timestamp": "2024-03-21T10:30:00Z"
            }
        }


class MessageHistory(BaseModel):
    """Single message in chat history"""
    id: str
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime
    tokens_used: int
    escalation_score: int


class ChatHistory(BaseModel):
    """Chat history schema"""
    session_id: str
    mode: ModeEnum
    messages: List[MessageHistory]
    total_messages: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
