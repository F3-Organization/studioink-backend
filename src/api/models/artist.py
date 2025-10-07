from django.conf import settings
from django.db import models

from api.models.studio import Studio

from .base import BaseModel


class ArtistProfile(BaseModel):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Dono"
        ARTIST = "ARTIST", "Artista"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_profile",
        verbose_name="Usuário",
    )
    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="artist_profiles",
        verbose_name="Estúdio",
    )
    bio = models.TextField(verbose_name="Biografia", blank=True, null=True)
    profile = models.ImageField(
        upload_to="artist_profiles/",
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ARTIST,
        verbose_name="Função",
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username
