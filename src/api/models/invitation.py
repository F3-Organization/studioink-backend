import uuid

from django.db import models

from api.models.base import BaseModel
from api.models.studio import Studio


class Invitation(BaseModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        ACCEPTED = "ACCEPTED", "Aceito"
        REJECTED = "REJECTED", "Rejeitado"

    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f"Convite para {self.email} no estúdio {self.studio.name}"

    @classmethod
    def create_invitation(cls, studio, email):
        invitation = cls.objects.create(studio=studio, email=email)
        return invitation
