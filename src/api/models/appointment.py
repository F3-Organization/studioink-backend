from django.db import models

from api.models.artist import ArtistProfile
from api.models.base import BaseModel
from api.models.client import Client
from api.models.studio import Studio


class Appointment(BaseModel):
    class AppointmentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        CONFIRMED = "CONFIRMED", "Confirmado"
        COMPLETED = "COMPLETED", "Concluído"
        CANCELED = "CANCELED", "Cancelado"

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Estúdio",
    )
    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Artista",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Cliente",
    )

    start_time = models.DateTimeField(verbose_name="Início do Agendamento")
    end_time = models.DateTimeField(verbose_name="Fim do Agendamento")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
        verbose_name="Status do Agendamento",
    )

    price_quoted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Orçado",
        null=True,
        blank=True,
    )
    deposit_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Depósito Pago",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.client.full_name} com {self.artist.user.username} em {self.start_time.strftime('%d/%m/%Y %H:%M')}"
