"""
Service Layer - Business Logic
Maps to: Implementation - Code Structure (Services / business logic)
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models import User, Message, Conversation
from app.schemas import UserCreate, MessageCreate
from app.auth import get_password_hash
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


# ==================== User Service ====================

class UserService:
    """
    User business logic
    Maps to: Requirements & Planning - Identify use cases and features
    """
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if username already exists
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send welcome email
        if settings.enable_email_notifications:
            try:
                from app.services.email_service import EmailService
                EmailService.send_welcome_email(db_user.email, db_user.username)
            except Exception as e:
                logger.warning(f"Failed to send welcome email: {str(e)}")
        
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()


# ==================== Conversation Service ====================

class ConversationService:
    """
    Conversation business logic
    Maps to: Implementation - Code Structure (Services / business logic)
    """
    
    @staticmethod
    def get_or_create_conversation(db: Session, user1_id: int, user2_id: int) -> Conversation:
        """
        Get existing conversation or create new one
        Maps to: Requirements & Planning - Identify reusable APIs
        """
        # Ensure user1_id < user2_id for consistency
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id
        
        # Check if conversation exists
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.user1_id == user1_id,
                Conversation.user2_id == user2_id
            )
        ).first()
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        return conversation
    
    @staticmethod
    def get_user_conversations(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """
        Get all conversations for a user
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        conversations = db.query(Conversation).filter(
            or_(
                Conversation.user1_id == user_id,
                Conversation.user2_id == user_id
            )
        ).offset(skip).limit(limit).all()
        
        return conversations
    
    @staticmethod
    def get_conversation_by_id(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """Get conversation by ID (only if user is participant)"""
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            or_(
                Conversation.user1_id == user_id,
                Conversation.user2_id == user_id
            )
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )
        
        return conversation


# ==================== Message Service ====================

class MessageService:
    """
    Message business logic
    Maps to: Implementation - Code Structure (Services / business logic)
    """
    
    @staticmethod
    def create_message(db: Session, message_data: MessageCreate, sender_id: int) -> Message:
        """
        Create a new message
        Maps to: Testing - Business logic
        """
        # Verify receiver exists
        receiver = UserService.get_user_by_id(db, message_data.receiver_id)
        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver not found"
            )
        
        # Prevent sending messages to self
        if sender_id == message_data.receiver_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot send message to yourself"
            )
        
        # Get or create conversation
        conversation = ConversationService.get_or_create_conversation(
            db, sender_id, message_data.receiver_id
        )
        
        # Create message
        db_message = Message(
            conversation_id=conversation.id,
            sender_id=sender_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # Send email notification to receiver
        if settings.enable_email_notifications:
            try:
                from app.services.email_service import EmailService
                sender = UserService.get_user_by_id(db, sender_id)
                # Get message preview (first 100 characters)
                message_preview = message_data.content[:100] if len(message_data.content) > 100 else message_data.content
                EmailService.send_new_message_notification(
                    receiver_email=receiver.email,
                    receiver_name=receiver.username,
                    sender_name=sender.username,
                    message_preview=message_preview
                )
            except Exception as e:
                logger.warning(f"Failed to send email notification: {str(e)}")
        
        return db_message
    
    @staticmethod
    def get_messages(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        conversation_id: Optional[int] = None
    ) -> List[Message]:
        """
        Get messages for a user
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        query = db.query(Message).filter(
            or_(
                Message.sender_id == user_id,
                Message.receiver_id == user_id
            )
        )
        
        if conversation_id:
            query = query.filter(Message.conversation_id == conversation_id)
        
        messages = query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
        return messages
    
    @staticmethod
    def get_message_by_id(db: Session, message_id: int, user_id: int) -> Optional[Message]:
        """Get message by ID (only if user is sender or receiver)"""
        message = db.query(Message).filter(
            Message.id == message_id,
            or_(
                Message.sender_id == user_id,
                Message.receiver_id == user_id
            )
        ).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found or access denied"
            )
        
        return message
    
    @staticmethod
    def mark_message_as_read(db: Session, message_id: int, user_id: int) -> Message:
        """Mark message as read (only receiver can do this)"""
        message = db.query(Message).filter(
            Message.id == message_id,
            Message.receiver_id == user_id
        ).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found or you are not the receiver"
            )
        
        message.is_read = True
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def get_conversation_messages(
        db: Session,
        conversation_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        """Get all messages in a conversation"""
        # Verify user is part of the conversation
        ConversationService.get_conversation_by_id(db, conversation_id, user_id)
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
        
        return messages
