import logging
import requests
from auth import settings
from django.contrib.auth import get_user_model
from celery import shared_task
from authent.models import CustomUser

# Configure logging
logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task
def send_email_verification(user_email, verification_url):
    logger.info(f"Task started: Sending verification email to {user_email}")
    try:
        email_data = {
            "sender": {"email": "ahad51860@gmail.com"},
            "to": [{"email": user_email}],
            "subject": "Email Verification",
            "htmlContent": f"<p>Hello,</p><p>Verify your email by clicking here:</p><a href=\"{verification_url}\">Verify Email</a>"
        }

        response = requests.post(
            settings.BREVO_EMAIL_ENDPOINT,
            headers={"api-key": settings.BRAVO_API_KEY, "Content-Type": "application/json"},
            json=email_data
        )
        if response.status_code == 201:
            logger.info("Verification email sent successfully.")
        else:
            logger.error(f"Failed to send email: {response.json()}")
    except Exception as e:
        logger.error("Error in sending email verification", exc_info=True)

    
@shared_task
def send_password_reset_email(email, reset_url, full_name):
    logger.info(f"Sending password reset email to {email}...")
    email_data = {
        "sender": {"email": "ahad51860@gmail.com"},
        "to": [{"email": email}],
        "subject": "Password Reset Request",
        "htmlContent": f"<p>Hello {full_name},</p><p>Click here to reset your password: <a href=\"{reset_url}\">Reset Password</a></p>"
    }

    try:
        response = requests.post(
            settings.BREVO_EMAIL_ENDPOINT,
            headers={"api-key": settings.BRAVO_API_KEY, "Content-Type": "application/json"},
            json=email_data
        )
        if response.status_code != 200:
            logger.error(f"Failed to send password reset email: {response.json()}")
    except Exception as e:
        logger.exception("Error occurred while sending the reset email.")

