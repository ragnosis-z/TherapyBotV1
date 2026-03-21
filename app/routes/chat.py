"""Chat routes"""

import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse, ChatHistory
from app.models import ChatSession, Message, User
from app.services import LLMService, EscalationService
from app.utils.safety import get_crisis_response
from app.utils.prompts import get_system_prompt

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize services
llm_service = LLMService()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """
    Send a message and get AI response

    Args:
        request: Chat request with message and optional session_id
        db: Database session

    Returns:
        ChatResponse with AI response and session details
    """
    try:
        # Get or create session
        session = None
        if request.session_id:
            session = db.query(ChatSession).filter(
                ChatSession.id == request.session_id
            ).first()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
        
        if not session:
            # Create new session
            session_id = str(uuid.uuid4())
            session = ChatSession(
                id=session_id,
                user_id="anonymous",  # Will be set with auth in later phase
                mode=request.mode,
            )
            db.add(session)
            db.commit()
            db.refresh(session)
        
        # Check for escalation
        escalation_service = EscalationService(db)
        is_escalation, escalation_type, crisis_response = await escalation_service.check_for_escalation(
            request.message,
            session.id,
            session.user_id,
        )
        
        # Generate response
        if is_escalation:
            response_text = crisis_response
            tokens_used = 0
        else:
            # Get conversation history
            history_messages = db.query(Message).filter(
                Message.session_id == session.id
            ).order_by(Message.created_at).all()
            
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in history_messages[-10:]  # Last 10 messages for context
            ]
            
            # Generate LLM response
            response_text, tokens_used = await llm_service.generate_response(
                request.message,
                session.mode,
                conversation_history,
            )
        
        # Save user message
        user_message = Message(
            id=str(uuid.uuid4()),
            session_id=session.id,
            role="user",
            content=request.message,
            tokens_used=0,
        )
        db.add(user_message)
        db.flush()
        
        # Save assistant message
        assistant_message = Message(
            id=str(uuid.uuid4()),
            session_id=session.id,
            role="assistant",
            content=response_text,
            tokens_used=tokens_used,
            model_used="gpt-4" if tokens_used > 0 else "template",
        )
        db.add(assistant_message)
        
        # Update session stats
        session.message_count += 2
        session.total_tokens_used += tokens_used
        session.updated_at = datetime.utcnow()
        
        db.commit()
        
        return ChatResponse(
            response=response_text,
            mode=session.mode,
            session_id=session.id,
            message_id=assistant_message.id,
            escalation_detected=is_escalation,
            escalation_type=escalation_type,
            tokens_used=tokens_used,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing message")


@router.get("/session/{session_id}/history", response_model=ChatHistory)
async def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
) -> ChatHistory:
    """
    Get chat history for a session

    Args:
        session_id: Session ID
        db: Database session

    Returns:
        ChatHistory with all messages
    """
    try:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at).all()
        
        return ChatHistory(
            session_id=session.id,
            mode=session.mode,
            messages=[
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at,
                    "tokens_used": msg.tokens_used,
                    "escalation_score": msg.escalation_score,
                }
                for msg in messages
            ],
            total_messages=len(messages),
            created_at=session.created_at,
            updated_at=session.updated_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving history")


@router.post("/session/create")
async def create_session(
    mode: str = "gentle_guide",
    db: Session = Depends(get_db),
):
    """
    Create a new chat session

    Args:
        mode: Therapeutic mode
        db: Database session

    Returns:
        Session details
    """
    try:
        session_id = str(uuid.uuid4())
        session = ChatSession(
            id=session_id,
            user_id="anonymous",
            mode=mode,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "session_id": session.id,
            "mode": session.mode,
            "created_at": session.created_at,
        }
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating session")


@router.post("/session/{session_id}/end")
async def end_session(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    End a chat session

    Args:
        session_id: Session ID
        db: Database session

    Returns:
        Success message
    """
    try:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session.is_active = False
        session.ended_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": "Session ended successfully",
            "session_id": session_id,
            "messages_count": session.message_count,
            "total_tokens": session.total_tokens_used,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ending session: {str(e)}")
        raise HTTPException(status_code=500, detail="Error ending session")


@router.get("/modes")
async def get_available_modes():
    """Get available therapeutic modes"""
    from app.utils.prompts import get_modes_description
    
    return {
        "modes": get_modes_description(),
        "default": "gentle_guide",
    }
