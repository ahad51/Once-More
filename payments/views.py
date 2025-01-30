import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from auth import settings
from authent.models import Teacher
from .models import Subscription
from .services import create_stripe_customer, create_stripe_subscription, cancel_stripe_subscription
from .tasks import send_admin_credentials_email

# Configure logging
logger = logging.getLogger(__name__)

# Ensure to use your custom user model
CustomUser = get_user_model()
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

CustomUser = get_user_model()



class SubscriptionView(APIView):
    def post(self, request):
        email = request.data.get("email")
        price_id = request.data.get("price_id")

        if not email or not price_id:
            return Response({"error": "Email and price_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if user exists, otherwise create a new one
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                username = email.split('@')[0]
                user = CustomUser.objects.create_user(username=username, email=email)

            # Check if the user already has an active subscription
            existing_subscription = Subscription.objects.filter(user=user).first()
            if existing_subscription:
                return Response(
                    {"error": "User already has an active subscription"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Make the user an admin
            user.is_staff = True
            user.is_superuser = False
            user.save()

            # Assign permissions to add, change, and view Teacher
            content_type = ContentType.objects.get_for_model(Teacher)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=["add_teacher", "change_teacher", "view_teacher"]
            )
            user.user_permissions.add(*permissions)

            # Step 2: Create Stripe customer and subscription
            customer = create_stripe_customer(email)
            subscription = create_stripe_subscription(customer["id"], price_id)

            # Step 3: Store subscription data in the database
            Subscription.objects.create(
                user=user,
                stripe_subscription_id=subscription["id"],
                stripe_customer_id=customer["id"]
            )

            send_admin_credentials_email.delay(user_id=user.id, admin_email=email)

            return Response(
                {
                    "subscription_id": subscription["id"],
                    "message": "Subscribed successfully. Check email for admin panel access."
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"Error processing subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def put(self, request):
        logger.info("Updating subscription...")
        subscription_id = request.data.get("subscription_id")
        price_id = request.data.get("price_id")

        # Check for missing parameters
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

        # Check for missing parameter
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
