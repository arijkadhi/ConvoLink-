"""
Tests for Email Service
Maps to: Testing - Business logic / External API Integration
"""
import pytest
from unittest.mock import Mock, patch
from app.services.email_service import EmailService


class TestEmailService:
    """Test email notification service"""
    
    @patch('app.services.email_service.SendGridAPIClient')
    @patch('app.services.email_service.settings')
    def test_send_new_message_notification_success(self, mock_settings, mock_sg_client):
        """Test successful email notification"""
        # Mock settings
        mock_settings.sendgrid_api_key = "test-api-key"
        mock_settings.sendgrid_from_email = "noreply@test.com"
        mock_settings.app_name = "Test Messaging API"
        mock_settings.app_url = "http://localhost:8000"
        
        # Mock SendGrid response
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_instance = Mock()
        mock_sg_instance.send.return_value = mock_response
        mock_sg_client.return_value = mock_sg_instance
        
        # Send notification
        result = EmailService.send_new_message_notification(
            receiver_email="receiver@test.com",
            receiver_name="Receiver",
            sender_name="Sender",
            message_preview="Hello, this is a test message"
        )
        
        assert result is True
        mock_sg_instance.send.assert_called_once()
    
    @patch('app.services.email_service.settings')
    def test_send_new_message_notification_no_api_key(self, mock_settings):
        """Test email notification when API key not configured"""
        mock_settings.sendgrid_api_key = "your-sendgrid-api-key-here"
        
        result = EmailService.send_new_message_notification(
            receiver_email="receiver@test.com",
            receiver_name="Receiver",
            sender_name="Sender",
            message_preview="Hello"
        )
        
        assert result is False
    
    @patch('app.services.email_service.SendGridAPIClient')
    @patch('app.services.email_service.settings')
    def test_send_new_message_notification_failure(self, mock_settings, mock_sg_client):
        """Test email notification failure"""
        mock_settings.sendgrid_api_key = "test-api-key"
        mock_settings.sendgrid_from_email = "noreply@test.com"
        mock_settings.app_name = "Test Messaging API"
        mock_settings.app_url = "http://localhost:8000"
        
        # Mock SendGrid failure
        mock_response = Mock()
        mock_response.status_code = 400
        mock_sg_instance = Mock()
        mock_sg_instance.send.return_value = mock_response
        mock_sg_client.return_value = mock_sg_instance
        
        result = EmailService.send_new_message_notification(
            receiver_email="receiver@test.com",
            receiver_name="Receiver",
            sender_name="Sender",
            message_preview="Hello"
        )
        
        assert result is False
    
    @patch('app.services.email_service.SendGridAPIClient')
    @patch('app.services.email_service.settings')
    def test_send_unread_messages_digest_success(self, mock_settings, mock_sg_client):
        """Test successful unread messages digest"""
        mock_settings.sendgrid_api_key = "test-api-key"
        mock_settings.sendgrid_from_email = "noreply@test.com"
        mock_settings.app_name = "Test Messaging API"
        mock_settings.app_url = "http://localhost:8000"
        
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_instance = Mock()
        mock_sg_instance.send.return_value = mock_response
        mock_sg_client.return_value = mock_sg_instance
        
        result = EmailService.send_unread_messages_digest(
            receiver_email="receiver@test.com",
            receiver_name="Receiver",
            unread_count=5,
            sender_names=["Sender1", "Sender2", "Sender3"]
        )
        
        assert result is True
    
    @patch('app.services.email_service.SendGridAPIClient')
    @patch('app.services.email_service.settings')
    def test_send_welcome_email_success(self, mock_settings, mock_sg_client):
        """Test successful welcome email"""
        mock_settings.sendgrid_api_key = "test-api-key"
        mock_settings.sendgrid_from_email = "noreply@test.com"
        mock_settings.app_name = "Test Messaging API"
        mock_settings.app_url = "http://localhost:8000"
        
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_instance = Mock()
        mock_sg_instance.send.return_value = mock_response
        mock_sg_client.return_value = mock_sg_instance
        
        result = EmailService.send_welcome_email(
            user_email="newuser@test.com",
            username="NewUser"
        )
        
        assert result is True
    
    @patch('app.services.email_service.SendGridAPIClient')
    @patch('app.services.email_service.settings')
    def test_send_email_with_exception(self, mock_settings, mock_sg_client):
        """Test email sending with exception"""
        mock_settings.sendgrid_api_key = "test-api-key"
        mock_settings.sendgrid_from_email = "noreply@test.com"
        mock_settings.app_name = "Test Messaging API"
        mock_settings.app_url = "http://localhost:8000"
        
        # Mock exception
        mock_sg_client.side_effect = Exception("SendGrid error")
        
        result = EmailService.send_new_message_notification(
            receiver_email="receiver@test.com",
            receiver_name="Receiver",
            sender_name="Sender",
            message_preview="Hello"
        )
        
        assert result is False
