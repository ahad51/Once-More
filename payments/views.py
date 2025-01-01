import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from auth import settings
from .models import Subscription
from .services import create_stripe_customer, create_stripe_subscription, cancel_stripe_subscription
from .tasks import send_admin_credentials_email
from django.utils.crypto import get_random_string

# Configure logging
logger = logging.getLogger(__name__)

# Ensure to use your custom user model
CustomUser = get_user_model()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import Subscription
from .tasks import send_admin_credentials_email
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Ensure to use your custom user model
CustomUser = get_user_model()


class SubscriptionView(APIView):
    def post(self, request):
        logger.info("Starting subscription process...")
        email = request.data.get("email")
        price_id = request.data.get("price_id")

        if not email or not price_id:
            logger.error("Missing required parameters: email or price_id")
            return Response({"error": "Email and price_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            logger.info(f"Checking if user with email {email} exists...")
            user = CustomUser.objects.filter(email=email).first()

            if not user:
                logger.info(f"User with email {email} does not exist. Creating a new user...")
                username = email.split('@')[0]  # Or generate a custom username
                
                user = CustomUser.objects.create_user(username=username, email=email)
                user.is_staff = True  # Make the user an admin
                user.is_superuser = True
                user.save()
                logger.info(f"User {user.email} created and set as admin.")
            else:
                user.save()
                logger.info(f"Password reset for existing user {user.email}")
                user.is_staff = True  # Make the user an admin
                user.is_superuser = True
                user.save()

            # Generate a random admin email
            random_email = f"admin_{get_random_string(8)}@example.com"
            logger.info(f"Generated random admin email: {random_email}")

            # Step 2: Create Stripe customer and subscription
            try:
                logger.info(f"Creating Stripe customer for {email}...")
                customer = create_stripe_customer(email)
                logger.info(f"Stripe customer created with ID {customer['id']}")
            except Exception as e:
                logger.error(f"Error creating Stripe customer: {e}")
                return Response({"error": "Failed to create Stripe customer."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                logger.info(f"Creating Stripe subscription for customer {customer['id']}...")
                subscription = create_stripe_subscription(customer["id"], price_id)
                logger.info(f"Stripe subscription created with ID {subscription['id']}")
            except Exception as e:
                logger.error(f"Error creating Stripe subscription: {e}")
                return Response({"error": "Failed to create Stripe subscription."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Step 3: Store subscription data in the database
            Subscription.objects.create(
                user=user,
                stripe_subscription_id=subscription["id"],
                stripe_customer_id=customer["id"]
            )
            logger.info("Subscription data stored in the database.")

            # Step 4: Send admin credentials email to the random email via Celery
            send_admin_credentials_email.delay(user_id=user.id, admin_email=user.email   )

            logger.info(f"Admin credentials email task sent to Celery for user {user.email}.")

            return Response(
                {
                    "subscription_id": subscription["id"],
                    "message": "Subscribed successfully. Check email for admin pannel access."
                },
                status=status.HTTP_201_CREATED
            )

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        logger.info("Updating subscription...")
        subscription_id = request.data.get("subscription_id")
        price_id = request.data.get("price_id")
        
        if not subscription_id or not price_id:
            logger.error("Missing required parameters: subscription_id or price_id")
            return Response({"error": "subscription_id and price_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            if not subscription['items']['data']:
                logger.error("No subscription items found.")
                return Response({"error": "No subscription items found."}, status=status.HTTP_400_BAD_REQUEST)

            subscription_item_id = subscription['items']['data'][0].id  # Assuming updating the first item
            
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription_item_id,
                    'price': price_id,
                }],
            )
            logger.info(f"Subscription {subscription_id} updated successfully.")
            return Response(updated_subscription, status=status.HTTP_200_OK)
        
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logger.info("Cancelling subscription...")
        subscription_id = request.data.get("subscription_id")
        
        if not subscription_id:
            logger.error("Missing required parameter: subscription_id")
            return Response({"error": "subscription_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cancel_stripe_subscription(subscription_id)
            logger.info(f"Subscription {subscription_id} canceled successfully.")
            return Response(
                {
                    "message": "Subscription canceled successfully"
                },
                status=status.HTTP_200_OK
            )
        
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
