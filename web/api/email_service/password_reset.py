from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.email_service.base import BaseEmailService


class PasswordResetService(BaseEmailService):
    template_name = 'emails/password_reset.html'

    @property
    def email_subject(self) -> str:
        return _('Blog password reset')

    def email_context(self, reset_url: str, **kwargs) -> dict:
        return {
            'full_name': self.user.full_name,
            'reset_url': reset_url,
        }
