from django.dispatch import receiver
from django.db.models.signals import post_save

from main.tasks import send_information_email
from .models import Feedback
from .services import ContactUsService


@receiver(post_save, sender=Feedback)
def send_emails(sender, created: bool, instance, **kwargs):
    if created:
        send_information_email.delay(**ContactUsService.get_admin_email_data(instance))
        send_information_email.delay(**ContactUsService.get_user_email_data(instance))
