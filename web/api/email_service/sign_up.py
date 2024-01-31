from django.utils.translation import gettext_lazy as _

from api.email_service.base import BaseEmailService


class SignUpEmailService(BaseEmailService):
    template_name = 'emails/verify_email.html'

    @property
    def email_subject(self) -> str:
        return _('Blog register confirmation email')

    def email_context(self, activate_url: str, **kwargs) -> dict:
        return {
            'full_name': self.user.full_name,
            'activate_url': activate_url,
        }
