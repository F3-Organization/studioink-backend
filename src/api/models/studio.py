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
