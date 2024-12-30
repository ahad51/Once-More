import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_customer(email):
    return stripe.Customer.create(email=email)

def create_stripe_subscription(customer_id, price_id):
    return stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        payment_behavior="default_incomplete",
        expand=["latest_invoice.payment_intent"]
    )

def update_stripe_subscription(subscription_id, price_id):
    return stripe.Subscription.modify(
        subscription_id,
        items=[{
            "id": subscription_id,
            "price": price_id
        }]
    )

def cancel_stripe_subscription(subscription_id):
    return stripe.Subscription.delete(subscription_id)

