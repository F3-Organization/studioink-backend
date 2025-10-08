from django.conf import settings
from django.db import models


class TermsAcceptance(models.Model):
    """
    Registra cada aceite dos Termos de Serviço por um usuário.
    Cria um log auditável e legalmente válido.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="terms_acceptances",
        verbose_name="Usuário",
    )
    terms_version = models.CharField(max_length=20, verbose_name="Versão dos Termos")
    acceptance_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Data do Aceite"
    )
    ip_address = models.GenericIPAddressField(
        blank=True, null=True, verbose_name="Endereço IP"
    )

    class Meta:
        verbose_name = "Aceite dos Termos"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "terms_version"),
                name="unique_user_terms_version",
            )
        ]

    def __str__(self):
        return f"Aceite dos Termos {self.terms_version} por {self.user.username} em {self.acceptance_date.strftime('%d/%m/%Y')}"

    @classmethod
    def create_terms_acceptance(cls, user, terms_version, ip_address=None):
        acceptance = cls.objects.create(
            user=user,
            terms_version=terms_version,
            ip_address=ip_address,
        )
        return acceptance
