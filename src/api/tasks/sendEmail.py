import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue="emails")
def send_invitation_email_task(subject, template_name, context, recipient_list):
    send_email(subject, template_name, context, recipient_list)


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
