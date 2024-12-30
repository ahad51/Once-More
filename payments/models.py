from django.db import models
from django.conf import settings
from stripe import api_key

api_key = "your-stripe-secret-key"

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.stripe_subscription_id}"
