"""
Message Tests
Maps to: Testing - Integration Tests (Endpoint behavior / Database interactions)
"""
import pytest
from fastapi import status


class TestMessages:
    """Test message endpoints"""
    
    def test_send_message(self, client, test_user, test_user2, auth_headers):
        """
        Test sending a message
        Maps to: Testing - Business logic
        """
        response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Hello, this is a test message!"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["content"] == "Hello, this is a test message!"
        assert data["sender_id"] == test_user.id
        assert data["receiver_id"] == test_user2.id
        assert data["is_read"] is False
    
    def test_send_message_to_nonexistent_user(self, client, test_user, auth_headers):
        """Test sending message to non-existent user"""
        response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": 9999,
                "content": "Test message"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_send_message_to_self(self, client, test_user, auth_headers):
        """Test sending message to self"""
        response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user.id,
                "content": "Message to myself"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_send_message_unauthorized(self, client, test_user2):
        """Test sending message without authentication"""
        response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_messages(self, client, test_user, test_user2, auth_headers, db):
        """
        Test retrieving messages
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        # Send a message first
        client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message 1"
            },
            headers=auth_headers
        )
        
        # Get messages
        response = client.get("/api/v1/messages/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert data[0]["content"] == "Test message 1"
    
    def test_get_message_by_id(self, client, test_user, test_user2, auth_headers):
        """Test retrieving a specific message"""
        # Send a message first
        send_response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message"
            },
            headers=auth_headers
        )
        message_id = send_response.json()["id"]
        
        # Get the message
        response = client.get(f"/api/v1/messages/{message_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == message_id
        assert data["content"] == "Test message"
    
    def test_get_message_unauthorized(self, client, test_user, test_user2, auth_headers, auth_headers2):
        """Test accessing message by unauthorized user"""
        # User 1 sends a message to User 2
        send_response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Private message"
            },
            headers=auth_headers
        )
        message_id = send_response.json()["id"]
        
        # Try to access with different user (should work for receiver)
        response = client.get(f"/api/v1/messages/{message_id}", headers=auth_headers2)
        assert response.status_code == status.HTTP_200_OK
    
    def test_mark_message_as_read(self, client, test_user, test_user2, auth_headers, auth_headers2):
        """Test marking message as read"""
        # User 1 sends a message to User 2
        send_response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message"
            },
            headers=auth_headers
        )
        message_id = send_response.json()["id"]
        
        # User 2 marks it as read
        response = client.patch(
            f"/api/v1/messages/{message_id}/read",
            headers=auth_headers2
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_read"] is True
    
    def test_pagination(self, client, test_user, test_user2, auth_headers):
        """Test message pagination"""
        # Send multiple messages
        for i in range(5):
            client.post(
                "/api/v1/messages/",
                json={
                    "receiver_id": test_user2.id,
                    "content": f"Message {i}"
                },
                headers=auth_headers
            )
        
        # Test pagination
        response = client.get("/api/v1/messages/?skip=0&limit=2", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
