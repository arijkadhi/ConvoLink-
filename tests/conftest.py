"""
Test Configuration
Maps to: Testing - Unit Tests & Integration Tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.auth import get_password_hash

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create database tables for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with database setup"""
    return TestClient(app)


@pytest.fixture
def test_user(db):
    """Create a test user"""
    from app.models import User
    
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("TestPassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user2(db):
    """Create a second test user"""
    from app.models import User
    
    user = User(
        username="testuser2",
        email="test2@example.com",
        hashed_password=get_password_hash("TestPassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "TestPassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers2(client, test_user2):
    """Get authentication headers for second test user"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser2", "password": "TestPassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
