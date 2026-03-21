"""User Request/Response Schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """User creation schema"""
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "jane_doe",
                "email": "jane@example.com",
                "password": "securepass123",
                "full_name": "Jane Doe"
            }
        }


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    primary_concerns: Optional[str] = None
    preferred_mode: Optional[str] = None
    support_contact_name: Optional[str] = None
    support_contact_phone: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    primary_concerns: Optional[str]
    preferred_mode: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "user_123",
                "username": "jane_doe",
                "email": "jane@example.com",
                "full_name": "Jane Doe",
                "is_active": True,
                "primary_concerns": None,
                "preferred_mode": "gentle_guide",
                "created_at": "2024-03-21T10:00:00Z",
                "last_login": None
            }
        }


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
