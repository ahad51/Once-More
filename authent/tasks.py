import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import Teacher

# Configure logging
logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task()
def send_teacher_credentials_email(teacher_id, plain_password):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        
        # Ensure the teacher has an associated user object with an email
        if teacher.user:
            teacher_email = teacher.user.email
        else:
            raise ValueError(f"Teacher with ID {teacher_id} does not have an associated user account.")

        # Prepare the email content
        email_data = {
            "sender": {"email": "ahad51860@gmail.com"},
            "to": [{"email": teacher_email}],
            "subject": "Your Teacher Account Credentials",
            "htmlContent": f"""
                <html>
                    <body>
                        <p>Dear {teacher.full_name},</p>
                        <p>Your teacher account has been created. Here are your login credentials:</p>
                        <p>Email: {teacher_email}</p>
                        <p>Password: {plain_password}</p>
                        <p>You can log in at: <a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a></p>
                    </body>
                </html>
            """,
            "textContent": f"""
                Dear {teacher.full_name},
                Your teacher account has been created. Here are your login credentials:
                Email: {teacher_email}
                Password: {plain_password}
                You can log in at: http://127.0.0.1:8000/
            """,
        }

        # Send the email via the API endpoint
        response = requests.post(
            settings.BREVO_EMAIL_ENDPOINT,
            headers={
                "api-key": settings.BRAVO_API_KEY,
                "Content-Type": "application/json",
            },
            json=email_data,
        )
        
        if response.status_code == 201:
            logger.info(f"Teacher credentials email successfully sent to {teacher_email}")
        else:
            # Log the failure response details
            logger.error(f"Failed to send teacher credentials email to {teacher_email}. Response: {response.status_code}")
            logger.error(f"Response body: {response.text}")
    
    except Teacher.DoesNotExist:
        logger.error(f"Teacher with ID {teacher_id} does not exist.")
    except requests.exceptions.Timeout:
        logger.error("Request to email API timed out.")
    except requests.exceptions.TooManyRedirects:
        logger.error("Too many redirects occurred while sending the email.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while sending the teacher credentials email: {e}", exc_info=True)
    except Exception as e:
        logger.error("Unexpected error occurred while sending the teacher credentials email", exc_info=True)
