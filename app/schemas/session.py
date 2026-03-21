"""Session Request/Response Schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.chat import ModeEnum


class SessionCreate(BaseModel):
    """Session creation schema"""
    mode: Optional[ModeEnum] = Field(default="gentle_guide")
    title: Optional[str] = None


class SessionUpdate(BaseModel):
    """Session update schema"""
    title: Optional[str] = None
    mode: Optional[ModeEnum] = None
    is_active: Optional[bool] = None


class SessionResponse(BaseModel):
    """Session response schema"""
    id: str
    user_id: str
    title: Optional[str]
    mode: ModeEnum
    is_active: bool
    message_count: int
    total_tokens_used: int
    escalation_detected: bool
    escalation_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "sess_123",
                "user_id": "user_456",
                "title": "Evening support",
                "mode": "companion",
                "is_active": True,
                "message_count": 12,
                "total_tokens_used": 1250,
                "escalation_detected": False,
                "escalation_reason": None,
                "created_at": "2024-03-21T10:00:00Z",
                "updated_at": "2024-03-21T10:30:00Z",
                "ended_at": None
            }
        }
