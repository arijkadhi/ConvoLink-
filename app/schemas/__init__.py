"""
Pydantic Schemas for Request/Response Validation
Maps to: API Design - Data Modeling (Response schemes / JSON structure / Field types and constraints)
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=50, description="Username for the user")
    email: EmailStr = Field(..., description="Email address of the user")


class UserCreate(UserBase):
    """
    Schema for user registration
    Maps to: Requirements & Planning - Identify use cases and features
    """
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    
    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class UserResponse(UserBase):
    """
    Schema for user response
    Maps to: API Design - Data Modeling (Response schemes / JSON structure)
    """
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Token Schemas ====================

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


# ==================== Message Schemas ====================

class MessageBase(BaseModel):
    """Base message schema"""
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")


class MessageCreate(MessageBase):
    """
    Schema for creating a message
    Maps to: API Design - Interaction Design (Filling, sorting / Authentication)
    """
    receiver_id: int = Field(..., description="ID of the message receiver")


class MessageUpdate(BaseModel):
    """Schema for updating message status"""
    is_read: bool


class MessageResponse(MessageBase):
    """
    Schema for message response
    Maps to: API Design - Data Modeling (Response schemes / JSON structure / Field types)
    """
    id: int
    conversation_id: int
    sender_id: int
    receiver_id: int
    is_read: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MessageWithUsers(MessageResponse):
    """Message response with sender/receiver details"""
    sender: UserResponse
    receiver: UserResponse


# ==================== Conversation Schemas ====================

class ConversationBase(BaseModel):
    """Base conversation schema"""
    pass


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation"""
    user2_id: int = Field(..., description="ID of the other user in the conversation")


class ConversationResponse(ConversationBase):
    """
    Schema for conversation response
    Maps to: Requirements & Planning - Identify reusable APIs
    """
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    """Conversation response with messages"""
    messages: List[MessageResponse] = []


class ConversationWithUsers(ConversationResponse):
    """Conversation response with user details"""
    user1: UserResponse
    user2: UserResponse
    last_message: Optional[MessageResponse] = None


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """
    Standardized error response
    Maps to: Documentation - Error catalog
    """
    error: str
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==================== Pagination Schemas ====================

class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=100, description="Maximum number of records to return")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    skip: int
    limit: int
    items: List
