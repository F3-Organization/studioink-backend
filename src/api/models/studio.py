from django.conf import settings
from django.db import models

from .base import BaseModel


class Studio(BaseModel):
    class SubscriptionPlan(models.TextChoices):
        SOLO = "SOLO", "Solo"
        STUDIO = "STUDIO", "Studio"

    class SubscriptionStatus(models.TextChoices):
        TRIALING = "TRIAL", "Em Teste"
        ACTIVE = "ACTIVE", "Ativo"
        FROZEN = "FROZEN", "Congelado"
        CANCELED = "CANCELED", "Cancelado"

    name = models.CharField(max_length=255, verbose_name="Nome do Estúdio")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_studios",
        verbose_name="Proprietário",
    )
    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.SOLO,
    )
    subscription_status = models.CharField(
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIALING,
    )

    def __str__(self):
        return self.name
