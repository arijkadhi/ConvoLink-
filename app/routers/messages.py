"""
Messages Router
Maps to: API Design - Resource & Endpoint Modeling (Choose endpoint patterns)
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import MessageCreate, MessageResponse, MessageWithUsers
from app.services import MessageService
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a new message
    Maps to: Requirements & Planning - Identify use cases and features
    Endpoint: POST /messages
    """
    return MessageService.create_message(db, message_data, current_user.id)


@router.get("/", response_model=List[MessageResponse])
def get_messages(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    conversation_id: Optional[int] = Query(None, description="Filter by conversation ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all messages for the current user
    Maps to: API Design - Resource & Endpoint Modeling (Choose endpoint patterns)
    Endpoint: GET /messages
    """
    return MessageService.get_messages(db, current_user.id, skip, limit, conversation_id)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific message by ID
    Maps to: Testing - Endpoint behavior / Database interactions
    Endpoint: GET /messages/{id}
    """
    return MessageService.get_message_by_id(db, message_id, current_user.id)


@router.patch("/{message_id}/read", response_model=MessageResponse)
def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark a message as read
    Maps to: API Design - Interaction Design (Filling, sorting / Authentication)
    """
    return MessageService.mark_message_as_read(db, message_id, current_user.id)
