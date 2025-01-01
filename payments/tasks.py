import logging
import requests
from auth import settings
from django.contrib.auth import get_user_model
from celery import shared_task
from authent.models import CustomUser

# Configure logging
logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task()
def send_admin_credentials_email(user_id, admin_email):
    try:
        # Retrieve the user
        user = CustomUser.objects.get(id=user_id)
        logger.info(f"User found: {user.email}")

        # Prepare email data for Brevo (Sendinblue)
        email_data = {
    "sender": {"email": "ahad51860@gmail.com"},  # Your sender email
    "to": [{"email": user.email}],  # Send to user's email
    "subject": "Admin Panel link",
    "htmlContent": f"""
        <html>
            <body>
                <p>Your Admin Panel Access:</p>
                <p><a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a></p>
                <p>Email: {admin_email}</p>
            </body>
        </html>
    """,
    "textContent": f"""
        Your Admin Panel Access:
        http://127.0.0.1:8000/admin/
        
        Email: {admin_email}
    """,
}


        # Send email via Brevo API
        response = requests.post(
            settings.BREVO_EMAIL_ENDPOINT,
            headers={
                "api-key": settings.BRAVO_API_KEY,
                "Content-Type": "application/json",
            },
            json=email_data,
        )

        # Check response status and log accordingly
        if response.status_code == 201:
            logger.info(f"Admin credentials email successfully sent to {user.email}")
        else:
            logger.error(f"Failed to send admin credentials email. Response: {response.status_code}")
            logger.error(f"Response body: {response.text}")

    except CustomUser.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while sending the admin credentials email", exc_info=True)
    except Exception as e:
        logger.error("Unexpected error occurred while sending the admin credentials email", exc_info=True)
