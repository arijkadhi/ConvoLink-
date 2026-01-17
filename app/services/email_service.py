"""
Email Notification Service using SendGrid
Maps to: Implementation - External API Integration (SendGrid for notifications)
"""
import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    """
    Email notification service using SendGrid API
    Maps to: Requirements & Planning - Identify reusable APIs
    """
    
    @staticmethod
    def send_new_message_notification(
        receiver_email: str,
        receiver_name: str,
        sender_name: str,
        message_preview: str
    ) -> bool:
        """
        Send email notification when user receives a new message
        
        Args:
            receiver_email: Email address of the message receiver
            receiver_name: Name of the receiver
            sender_name: Name of the message sender
            message_preview: Preview of the message content (first 100 chars)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Check if SendGrid is configured
        if not settings.sendgrid_api_key or settings.sendgrid_api_key == "your-sendgrid-api-key-here":
            logger.warning("SendGrid API key not configured. Email notification skipped.")
            return False
        
        try:
            # Create email message
            message = Mail(
                from_email=Email(settings.sendgrid_from_email, settings.app_name),
                to_emails=To(receiver_email, receiver_name),
                subject=f"New message from {sender_name}",
                html_content=Content(
                    "text/html",
                    f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                <h2 style="color: #4CAF50;">New Message Received!</h2>
                                <p>Hi {receiver_name},</p>
                                <p>You have received a new message from <strong>{sender_name}</strong>:</p>
                                <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
                                    <p style="margin: 0; font-style: italic;">"{message_preview}..."</p>
                                </div>
                                <p>
                                    <a href="{settings.app_url}/messages" 
                                       style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; 
                                              color: white; text-decoration: none; border-radius: 5px;">
                                        View Message
                                    </a>
                                </p>
                                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                                <p style="color: #888; font-size: 12px;">
                                    This is an automated notification from {settings.app_name}. 
                                    Please do not reply to this email.
                                </p>
                            </div>
                        </body>
                    </html>
                    """
                )
            )
            
            # Send email using SendGrid
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email notification sent to {receiver_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False
    
    @staticmethod
    def send_unread_messages_digest(
        receiver_email: str,
        receiver_name: str,
        unread_count: int,
        sender_names: list
    ) -> bool:
        """
        Send daily digest of unread messages
        
        Args:
            receiver_email: Email address of the receiver
            receiver_name: Name of the receiver
            unread_count: Number of unread messages
            sender_names: List of sender names
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Check if SendGrid is configured
        if not settings.sendgrid_api_key or settings.sendgrid_api_key == "your-sendgrid-api-key-here":
            logger.warning("SendGrid API key not configured. Email digest skipped.")
            return False
        
        try:
            sender_list = ", ".join(sender_names[:3])  # Show first 3 senders
            if len(sender_names) > 3:
                sender_list += f" and {len(sender_names) - 3} others"
            
            message = Mail(
                from_email=Email(settings.sendgrid_from_email, settings.app_name),
                to_emails=To(receiver_email, receiver_name),
                subject=f"You have {unread_count} unread message{'s' if unread_count > 1 else ''}",
                html_content=Content(
                    "text/html",
                    f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                <h2 style="color: #4CAF50;">Unread Messages Summary</h2>
                                <p>Hi {receiver_name},</p>
                                <p>You have <strong>{unread_count}</strong> unread message{'s' if unread_count > 1 else ''} from:</p>
                                <p style="font-size: 16px; color: #555;">{sender_list}</p>
                                <p>
                                    <a href="{settings.app_url}/messages" 
                                       style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; 
                                              color: white; text-decoration: none; border-radius: 5px;">
                                        Read Your Messages
                                    </a>
                                </p>
                                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                                <p style="color: #888; font-size: 12px;">
                                    This is an automated daily digest from {settings.app_name}.
                                </p>
                            </div>
                        </body>
                    </html>
                    """
                )
            )
            
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email digest sent to {receiver_email}")
                return True
            else:
                logger.error(f"Failed to send email digest. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email digest: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email: str, username: str) -> bool:
        """
        Send welcome email to newly registered users
        
        Args:
            user_email: Email address of the new user
            username: Username of the new user
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Check if SendGrid is configured
        if not settings.sendgrid_api_key or settings.sendgrid_api_key == "your-sendgrid-api-key-here":
            logger.warning("SendGrid API key not configured. Welcome email skipped.")
            return False
        
        try:
            message = Mail(
                from_email=Email(settings.sendgrid_from_email, settings.app_name),
                to_emails=To(user_email, username),
                subject=f"Welcome to {settings.app_name}!",
                html_content=Content(
                    "text/html",
                    f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                <h2 style="color: #4CAF50;">Welcome to {settings.app_name}!</h2>
                                <p>Hi {username},</p>
                                <p>Thank you for registering! Your account has been successfully created.</p>
                                <p>You can now:</p>
                                <ul>
                                    <li>Send and receive messages</li>
                                    <li>Manage your conversations</li>
                                    <li>Connect with other users</li>
                                </ul>
                                <p>
                                    <a href="{settings.app_url}/login" 
                                       style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; 
                                              color: white; text-decoration: none; border-radius: 5px;">
                                        Start Messaging
                                    </a>
                                </p>
                                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                                <p style="color: #888; font-size: 12px;">
                                    If you didn't create this account, please ignore this email.
                                </p>
                            </div>
                        </body>
                    </html>
                    """
                )
            )
            
            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Welcome email sent to {user_email}")
                return True
            else:
                logger.error(f"Failed to send welcome email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}")
            return False
