"""
Unit Tests for Services
Maps to: Testing - Unit Tests (Business logic)
"""
import pytest
from fastapi import HTTPException
from app.services import UserService, MessageService, ConversationService
from app.schemas import UserCreate, MessageCreate
from app.models import User


class TestUserService:
    """Test user service logic"""
    
    def test_create_user(self, db):
        """Test creating a new user"""
        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com",
            password="Password123"
        )
        user = UserService.create_user(db, user_data)
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.hashed_password != "Password123"  # Should be hashed
    
    def test_create_duplicate_user(self, db, test_user):
        """Test creating user with duplicate username"""
        user_data = UserCreate(
            username="testuser",
            email="another@example.com",
            password="Password123"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            UserService.create_user(db, user_data)
        assert exc_info.value.status_code == 400
    
    def test_get_user_by_username(self, db, test_user):
        """Test retrieving user by username"""
        user = UserService.get_user_by_username(db, "testuser")
        assert user is not None
        assert user.username == "testuser"
    
    def test_get_user_by_id(self, db, test_user):
        """Test retrieving user by ID"""
        user = UserService.get_user_by_id(db, test_user.id)
        assert user is not None
        assert user.id == test_user.id


class TestConversationService:
    """Test conversation service logic"""
    
    def test_get_or_create_conversation(self, db, test_user, test_user2):
        """Test creating a conversation"""
        conversation = ConversationService.get_or_create_conversation(
            db, test_user.id, test_user2.id
        )
        
        assert conversation.id is not None
        assert conversation.user1_id == min(test_user.id, test_user2.id)
        assert conversation.user2_id == max(test_user.id, test_user2.id)
    
    def test_get_existing_conversation(self, db, test_user, test_user2):
        """Test retrieving existing conversation"""
        # Create conversation
        conv1 = ConversationService.get_or_create_conversation(
            db, test_user.id, test_user2.id
        )
        
        # Try to create again (should return existing)
        conv2 = ConversationService.get_or_create_conversation(
            db, test_user.id, test_user2.id
        )
        
        assert conv1.id == conv2.id
    
    def test_get_user_conversations(self, db, test_user, test_user2):
        """Test retrieving user conversations"""
        # Create a conversation
        ConversationService.get_or_create_conversation(db, test_user.id, test_user2.id)
        
        # Get conversations
        conversations = ConversationService.get_user_conversations(db, test_user.id)
        assert len(conversations) == 1


class TestMessageService:
    """Test message service logic"""
    
    def test_create_message(self, db, test_user, test_user2):
        """Test creating a message"""
        message_data = MessageCreate(
            receiver_id=test_user2.id,
            content="Test message content"
        )
        
        message = MessageService.create_message(db, message_data, test_user.id)
        
        assert message.id is not None
        assert message.sender_id == test_user.id
        assert message.receiver_id == test_user2.id
        assert message.content == "Test message content"
        assert message.is_read is False
    
    def test_create_message_to_nonexistent_user(self, db, test_user):
        """Test creating message to non-existent user"""
        message_data = MessageCreate(
            receiver_id=9999,
            content="Test message"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            MessageService.create_message(db, message_data, test_user.id)
        assert exc_info.value.status_code == 404
    
    def test_create_message_to_self(self, db, test_user):
        """Test creating message to self"""
        message_data = MessageCreate(
            receiver_id=test_user.id,
            content="Message to self"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            MessageService.create_message(db, message_data, test_user.id)
        assert exc_info.value.status_code == 400
    
    def test_get_messages(self, db, test_user, test_user2):
        """Test retrieving messages"""
        # Create a message
        message_data = MessageCreate(
            receiver_id=test_user2.id,
            content="Test message"
        )
        MessageService.create_message(db, message_data, test_user.id)
        
        # Get messages
        messages = MessageService.get_messages(db, test_user.id)
        assert len(messages) == 1
        assert messages[0].content == "Test message"
    
    def test_mark_message_as_read(self, db, test_user, test_user2):
        """Test marking message as read"""
        # Create a message
        message_data = MessageCreate(
            receiver_id=test_user2.id,
            content="Test message"
        )
        message = MessageService.create_message(db, message_data, test_user.id)
        
        # Mark as read (by receiver)
        updated_message = MessageService.mark_message_as_read(
            db, message.id, test_user2.id
        )
        assert updated_message.is_read is True
