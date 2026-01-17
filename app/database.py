"""
Database Configuration
Maps to: Implementation - Database setup and connection
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    Maps to: Implementation - Dependency injection pattern
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    Maps to: Deployment - Database migrations
    """
    # Import all models here to ensure they are registered with Base
    from app.models import User, Message, Conversation
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
