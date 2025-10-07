from django.db import models

from api.models.base import BaseModel
from api.models.studio import Studio


class Client(BaseModel):
    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Estúdio",
    )
    full_name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email", unique=True)
    phone_number = models.CharField(max_length=20, verbose_name="Número de Telefone")
    date_of_birth = models.DateField(
        verbose_name="Data de Nascimento", null=True, blank=True
    )
    notes = models.TextField(
        verbose_name="Observações (alergias, etc...)", blank=True, null=True
    )

    class Meta:
        unique_together = ("studio", "email")
        unique_together = ("studio", "phone_number")

    def __str__(self):
        return self.full_name
