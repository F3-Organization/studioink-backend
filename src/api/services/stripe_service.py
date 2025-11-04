from os import getenv

from stripe import StripeClient, StripeError, Subscription


class StripeService:
    def __init__(self):
        self.stripeClient = StripeClient(getenv("STRIPE_API_KEY"))

    def create_customer(self, name: str, email: str, address: dict) -> Subscription:
        try:
            customer = self.stripeClient.v1.customers.create(
                params={
                    "name": name,
                    "email": email,
                    "shipping": {
                        "address": address,
                        "name": name,
                    },
                    "address": address,
                },
                options={"idempotency_key": f"customer-{email}"},
            )
            return customer
        except StripeError as e:
            print(f"Stripe error occurred: {e.user_message}")
            raise Exception("Failed to create customer in Stripe: ", e.user_message)

    def create_subscription(self, customer_id: str, price_id: str) -> Subscription:
        try:
            subscription = self.stripeClient.v1.subscriptions.create(
                params={
                    "customer": customer_id,
                    "items": [{"price": price_id}],
                    "payment_behavior": "default_incomplete",
                    "payment_settings": {
                        "save_default_payment_method": "on_subscription"
                    },
                    "billing_mode": {"type": "subscription"},
                    "expand": ["latest_invoice.confirmation_secret"],
                },
                options={"idempotency_key": f"subscription-{customer_id}-{price_id}"},
            )
            return subscription
        except StripeError as e:
            print(f"Stripe error occurred: {e.user_message}")
            raise Exception("Failed to create subscription in Stripe: ", e.user_message)

    def create_subscription_with_trial(
        self, customer_id: str, price_id: str, trial_days: int
    ) -> Subscription:
        try:
            subscription = self.stripeClient.v1.subscriptions.create(
                params={
                    "customer": customer_id,
                    "items": [{"price": price_id}],
                    "trial_period_days": trial_days,
                    "payment_behavior": "default_incomplete",
                    "payment_settings": {
                        "save_default_payment_method": "on_subscription"
                    },
                    "billing_mode": {"type": "subscription"},
                    "expand": ["latest_invoice.confirmation_secret"],
                },
                options={"idempotency_key": f"subscription-{customer_id}-{price_id}"},
            )
            return subscription
        except StripeError as e:
            print(f"Stripe error occurred: {e.user_message}")
            raise Exception("Failed to create subscription in Stripe: ", e.user_message)

    def retrieve_customer(self, customer_id: str):
        try:
            customer = self.stripeClient.v1.customers.retrieve(
                customer=customer_id, params={"expand": ["subscriptions"]}
            )
            return customer
        except StripeError as e:
            print(f"Stripe error occurred: {e.user_message}")
            raise Exception("Failed to retrieve customer in Stripe: ", e.user_message)
