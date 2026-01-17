"""
Database Models
Maps to: API Design - Data Modeling (Response schemes / JSON structure / Field types and constraints)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model for authentication
    Maps to: Requirements & Planning - Identify use cases and features
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    conversations_as_user1 = relationship("Conversation", foreign_keys="Conversation.user1_id", back_populates="user1")
    conversations_as_user2 = relationship("Conversation", foreign_keys="Conversation.user2_id", back_populates="user2")


class Conversation(Base):
    """
    Conversation model to group messages between two users
    Maps to: API Design - Resource & Endpoint Modeling (Define resources)
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="conversations_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="conversations_as_user2")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_conversation_users', 'user1_id', 'user2_id'),
    )


class Message(Base):
    """
    Message model for storing messages
    Maps to: API Design - Data Modeling (Response schemes / JSON structure)
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    conversation = relationship("Conversation", back_populates="messages")
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_message_conversation', 'conversation_id'),
        Index('idx_message_sender', 'sender_id'),
        Index('idx_message_receiver', 'receiver_id'),
    )
