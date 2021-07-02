from django.conf import settings
from rest_framework.reverse import reverse


class ContactUsService:

    @staticmethod
    def reverse_review_feedback_link(instance) -> str:
        app_name = instance._meta.app_label
        url = reverse(f"admin:{app_name}_feedback_change", args=(instance.id,))
        return settings.BACKEND_SITE + url

    @staticmethod
    def get_admin_email_data(feedback) -> dict:
        return {
            'to_email': settings.ADMIN_EMAILS,
            'subject': 'New feedback',
            'html_email_template_name': 'emails/admin_email.html',
            'file_url': feedback.file.url,
            'context': {
                'feedback_url': ContactUsService.reverse_review_feedback_link(feedback),
            },
        }

    @staticmethod
    def get_user_email_data(feedback) -> dict:
        return {
            'to_email': feedback.email,
            'subject': 'Thank You for your feedback',
            'html_email_template_name': 'emails/user_email.html',
            'context': {
                'user': feedback.name,
            },
        }
