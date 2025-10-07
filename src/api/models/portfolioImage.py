from django.db import models

from api.models.artist import ArtistProfile
from api.models.base import BaseModel


class PortfolioImage(BaseModel):
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name="portfolio_images",
        verbose_name="Artista",
    )
    image = models.ImageField(
        upload_to="portfolio_images/", verbose_name="Imagem do Portfólio"
    )
    title = models.CharField(max_length=255, verbose_name="Título", blank=True)
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)

    def __str__(self):
        return f"Imagem de {self.artist.user.username} - {self.title or 'Sem Título'}"
