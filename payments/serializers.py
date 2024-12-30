from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["stripe_customer_id", "stripe_subscription_id", "is_active", "start_date", "end_date"]
