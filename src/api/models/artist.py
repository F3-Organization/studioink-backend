from django.conf import settings
from django.db import models

from api.models.studio import Studio

from .base import BaseModel


class ArtistProfileQueryset(models.QuerySet["ArtistProfile"]):
    pass


class ArtistProfileManager(models.Manager):
    def is_owner_other_studio(self, email, current_studio):
        return (
            self.get_queryset()
            .filter(
                studio__owner__email__iexact=email,
                studio__subscription_plan=Studio.SubscriptionPlan.STUDIO,
            )
            .exclude(studio=current_studio)
            .exists()
        )

    def is_available_to_invite(self, studio, email):
        artist = self.get_queryset().filter(studio=studio, user__email=email).exists()
        return not artist


class ArtistProfile(BaseModel):
    objects: ArtistProfileManager | ArtistProfileQueryset = (
        ArtistProfileManager.from_queryset(ArtistProfileQueryset)()
    )

    class Role(models.TextChoices):
        OWNER = "OWNER", "Dono"
        ARTIST = "ARTIST", "Artista"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_profiles",
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

    class Meta:
        unique_together = ("user", "studio")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
