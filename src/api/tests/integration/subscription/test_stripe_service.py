from os import getenv

import pytest
from django.contrib.auth.models import User

from api.services.subscription.stripe_service import StripeService


@pytest.mark.skipif(not getenv("STRIPE_API_KEY"), reason="Stripe API key not set")
class TestStripeService:

    def test_stripe_service_create_customer(
        self, stripeService: StripeService, user: User, address: dict[str, str]
    ):
        customer = stripeService.create_customer(
            user.get_full_name(), user.email, address
        )
        assert customer is not None

    def test_create_subscription(
        self,
        stripeService: StripeService,
        customer_id: str,
        price_id: str,
    ):
        subscription = stripeService.create_subscription(customer_id, price_id)
        assert subscription is not None

    def test_create_subscription_with_trial(
        self,
        stripeService: StripeService,
        customer_id: str,
        price_id: str,
        trial_days: int,
    ):
        subscription = stripeService.create_subscription_with_trial(
            customer_id, price_id, trial_days
        )
        assert subscription is not None

    def test_retrieve_customer(
        self,
        stripeService: StripeService,
        customer_id: str,
    ):
        customer = stripeService.stripeClient.v1.customers.retrieve(customer_id)
        assert customer is not None
