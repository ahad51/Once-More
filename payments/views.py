from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from .services import create_stripe_customer, create_stripe_subscription, update_stripe_subscription, cancel_stripe_subscription

class SubscriptionView(APIView):
    
    def post(self, request):
        email = request.data.get("email")
        price_id = request.data.get("price_id")
        
        if not email or not price_id:
            return Response({"error": "Email and price_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer = create_stripe_customer(email)
            subscription = create_stripe_subscription(customer["id"], price_id)
            return Response(subscription, status=status.HTTP_201_CREATED)
        
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        subscription_id = request.data.get("subscription_id")
        price_id = request.data.get("price_id")
        
        if not subscription_id or not price_id:
            return Response({"error": "subscription_id and price_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            if not subscription['items']['data']:
                return Response({"error": "No subscription items found."}, status=status.HTTP_400_BAD_REQUEST)

            subscription_item_id = subscription['items']['data'][0].id  # Assuming updating the first item
            
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription_item_id,
                    'price': price_id,
                }],
            )
            return Response(updated_subscription, status=status.HTTP_200_OK)
        
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        subscription_id = request.data.get("subscription_id")
        
        if not subscription_id:
            return Response({"error": "subscription_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            canceled_subscription = cancel_stripe_subscription(subscription_id)
            return Response(canceled_subscription, status=status.HTTP_200_OK)
        
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
