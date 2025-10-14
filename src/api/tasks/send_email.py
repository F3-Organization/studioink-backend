import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.exceptions import APIException

from api.models.invitation import Invitation

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue="emails")
def send_invitation_email_task(self, invitation_id: int):
    try:
        invitation = Invitation.objects.select_related("studio").get(id=invitation_id)
    except Invitation.DoesNotExist:
        logger.error("Invitation with id %s not found. Skipping email.", invitation_id)
        return APIException("Invitation not found.", code=status.HTTP_404_NOT_FOUND)

    subject = f"Você foi convidado para se juntar ao studio {invitation.studio.name}!"
    template_name = "emails/invitation_email.html"
    context = {
        "studio_name": invitation.studio.name,
        "invitation_token": invitation.token,
        "accept_url": f"{settings.FRONTEND_URL}/accept-invitation/{invitation.token}",
    }
    recipient_list = [invitation.email]
    try:
        send_email(subject, template_name, context, recipient_list)
    except Exception as exc:
        logger.error(f"Error sending invitation email: {exc}")
        raise self.retry(exc=exc)


def send_email(subject, template_name, context, recipient_list):
    """
    Send an email using a specified template and context.
    """
    try:
        email_html_content = render_to_string(template_name, context)
        email_text_content = render_to_string(
            template_name.replace(".html", ".txt"), context
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=email_text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.attach_alternative(email_html_content, "text/html")

        email.send()
        logger.info(
            f"Email sent to {', '.join(recipient_list)} with subject '{subject}'"
        )
    except Exception as e:
        logger.error(f"Failed to send email to {', '.join(recipient_list)}: {e}")
        raise Exception(f"Error sending email: {e}")
