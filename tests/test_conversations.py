"""
Conversation Tests
Maps to: Testing - Integration Tests (Endpoint behavior / Database interactions)
"""
import pytest
from fastapi import status


class TestConversations:
    """Test conversation endpoints"""
    
    def test_create_conversation_via_message(self, client, test_user, test_user2, auth_headers):
        """
        Test that sending a message creates a conversation
        Maps to: Testing - Business logic
        """
        # Send a message (this should create a conversation)
        response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "First message"
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify conversation was created
        conv_response = client.get("/api/v1/conversations/", headers=auth_headers)
        assert conv_response.status_code == status.HTTP_200_OK
        conversations = conv_response.json()
        assert len(conversations) == 1
    
    def test_get_conversations(self, client, test_user, test_user2, auth_headers):
        """
        Test retrieving all conversations
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        # Send a message to create a conversation
        client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message"
            },
            headers=auth_headers
        )
        
        # Get conversations
        response = client.get("/api/v1/conversations/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert "user1" in data[0]
        assert "user2" in data[0]
    
    def test_get_conversation_by_id(self, client, test_user, test_user2, auth_headers):
        """Test retrieving a specific conversation"""
        # Send a message to create a conversation
        msg_response = client.post(
            "/api/v1/messages/",
            json={
                "receiver_id": test_user2.id,
                "content": "Test message"
            },
            headers=auth_headers
        )
        conversation_id = msg_response.json()["conversation_id"]
        
        # Get the conversation
        response = client.get(f"/api/v1/conversations/{conversation_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == conversation_id
    
    def test_get_conversation_messages(self, client, test_user, test_user2, auth_headers):
        """
        Test retrieving all messages in a conversation
        Maps to: Testing - Endpoint behavior / Database interactions
        """
        # Send multiple messages
        for i in range(3):
            client.post(
                "/api/v1/messages/",
                json={
                    "receiver_id": test_user2.id,
                    "content": f"Message {i}"
                },
                headers=auth_headers
            )
        
        # Get conversation
        conv_response = client.get("/api/v1/conversations/", headers=auth_headers)
        conversation_id = conv_response.json()[0]["id"]
        
        # Get conversation messages
        response = client.get(
            f"/api/v1/conversations/{conversation_id}/messages",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        messages = response.json()
        assert len(messages) == 3
    
    def test_conversation_unauthorized(self, client, test_user, test_user2, auth_headers, db):
        """Test accessing conversation without authentication"""
        # Create a conversation
        from app.models import Conversation
        conversation = Conversation(user1_id=test_user.id, user2_id=test_user2.id)
        db.add(conversation)
        db.commit()
        
        # Try to access without auth
        response = client.get(f"/api/v1/conversations/{conversation.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_conversation_messages_pagination(self, client, test_user, test_user2, auth_headers):
        """Test conversation messages pagination"""
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
        
        # Get conversation
        conv_response = client.get("/api/v1/conversations/", headers=auth_headers)
        conversation_id = conv_response.json()[0]["id"]
        
        # Test pagination
        response = client.get(
            f"/api/v1/conversations/{conversation_id}/messages?skip=0&limit=2",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        messages = response.json()
        assert len(messages) == 2
