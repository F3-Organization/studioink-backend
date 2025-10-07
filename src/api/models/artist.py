from django.conf import settings
from django.db import models

from .base import BaseModel


class ArtistProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_profile",
        verbose_name="Usuário",
    )
