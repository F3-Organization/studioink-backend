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
        constraints = [
            models.UniqueConstraint(
                fields=("studio", "email"), name="unique_studio_email"
            ),
            models.UniqueConstraint(
                fields=("studio", "phone_number"), name="unique_studio_phone"
            ),
        ]

    def __str__(self):
        return self.full_name
