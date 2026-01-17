"""
Authentication Tests
Maps to: Testing - Integration Tests (Endpoint behavior / Database interactions)
"""
import pytest
from fastapi import status


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client):
        """
        Test user registration
        Maps to: Testing - Business logic
        """
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "NewPassword123"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registering with duplicate username"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "another@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registering with duplicate email"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_weak_password(self, client):
        """Test registering with weak password"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "weak"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_success(self, client, test_user):
        """
        Test successful login
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "TestPassword123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "Password123"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "WrongPassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, client, test_user, auth_headers):
        """Test getting current user information"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
