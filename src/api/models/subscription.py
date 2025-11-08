from django.db import models

from api.models.base import BaseModel
from api.models.studio import Studio


class Subscription(BaseModel):
    class StatusChoices(models.TextChoices):
        TRIALING = "TRIALING", "Trialing"
        ACTIVE = "ACTIVE", "Active"
        INCOMPLETE = "INCOMPLETE", "Incomplete"
        INCOMPLETE_EXPIRED = "INCOMPLETE_EXPIRED", "Incomplete Expired"
        PAST_DUE = "PAST_DUE", "Past Due"
        CANCELED = "CANCELED", "Canceled"
        UNPAID = "UNPAID", "Unpaid"
        PAUSED = "PAUSED", "Paused"

    studio = models.OneToOneField(
        Studio,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TRIALING,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    price_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return (
            f"Subscription {self.stripe_subscription_id} for Studio {self.studio.name}"
        )
