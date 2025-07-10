from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email(subject, message, from_email, recipient_list, html_message=None):
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
