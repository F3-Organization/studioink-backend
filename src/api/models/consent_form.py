import uuid

from django.db import models

from api.models.appointment import Appointment
from api.models.base import BaseModel
from api.models.client import Client


class ConsentForm(BaseModel):
    class FormType(models.TextChoices):
        ANAMNESIS = "ANAM", "Anamnese"
        CONSENT_TERM = "CONS", "Termo de Consentimento"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="forms",
    )
    appointment = models.ForeignKey(
        Appointment,
        null=True,
        on_delete=models.SET_NULL,
    )
    form_type = models.CharField(max_length=4, choices=FormType.choices)

    unique_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    form_data = models.JSONField(default=dict)  # Respostas da anamnese

    signed_at = models.DateTimeField(null=True, blank=True)
    signature_data = models.TextField(blank=True)  # base64 da assinatura
    pdf_file = models.FileField(upload_to="consent_forms/%Y/%m/", null=True, blank=True)

    def get_form_link(self):
        return f"/formulario/{self.unique_token}/"
