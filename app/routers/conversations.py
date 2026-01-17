"""
Conversations Router
Maps to: Requirements & Planning - Identify reusable APIs
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    ConversationResponse,
    ConversationWithUsers,
    MessageResponse,
    UserResponse
)
from app.services import ConversationService, MessageService
from app.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/", response_model=List[ConversationWithUsers])
def get_conversations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all conversations for the current user
    Maps to: API Design - Resource & Endpoint Modeling (Define resources)
    Endpoint: GET /conversations
    """
    conversations = ConversationService.get_user_conversations(db, current_user.id, skip, limit)
    
    # Enrich with user details and last message
    result = []
    for conv in conversations:
        conv_dict = {
            "id": conv.id,
            "user1_id": conv.user1_id,
            "user2_id": conv.user2_id,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "user1": UserResponse.from_orm(conv.user1),
            "user2": UserResponse.from_orm(conv.user2),
            "last_message": None
        }
        
        # Get last message
        messages = MessageService.get_conversation_messages(db, conv.id, current_user.id, skip=0, limit=1)
        if messages:
            conv_dict["last_message"] = MessageResponse.from_orm(messages[-1])
        
        result.append(conv_dict)
    
    return result


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific conversation by ID
    Maps to: Testing - Endpoint behavior / Database interactions
    """
    return ConversationService.get_conversation_by_id(db, conversation_id, current_user.id)


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all messages in a conversation
    Maps to: API Design - Resource & Endpoint Modeling (Choose endpoint patterns)
    Endpoint: GET /conversations/{id}/messages
    """
    return MessageService.get_conversation_messages(db, conversation_id, current_user.id, skip, limit)
