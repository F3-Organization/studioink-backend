from django.db import models

from api.models.appointment import Appointment
from api.models.base import BaseModel
from api.models.client import Client


class ClientPhoto(BaseModel):
    class PhotoType(models.TextChoices):
        REFERENCE = "REF", "Referência"
        COMPLETED = "DONE", "Trabalho Concluído"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    appointment = models.ForeignKey(
        Appointment, null=True, blank=True, on_delete=models.SET_NULL
    )
    photo = models.ImageField(upload_to="client_photos/%Y/%m/")
    photo_type = models.CharField(max_length=4, choices=PhotoType.choices)
    description = models.TextField(blank=True)
