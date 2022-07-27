import re

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from main.decorators import except_shell
from main.tasks import send_information_email
from .utils import get_client_ip

User = get_user_model()


class CeleryService:

    @staticmethod
    def send_password_reset(content: dict, to_email: str):
        content: dict = {
            'subject': _('Password Reset'),
            'html_email_template_name': 'emails/password_reset.html',
            'to_email': to_email,
            'context': content,
        }
        send_information_email.delay(**content)

    @staticmethod
    def send_email_confirm(user):
        content: dict = {
            'subject': _('Please Confirm Your E-mail Address'),
            'html_email_template_name': 'emails/verify_email.html',
            'to_email': user.email,
            'context': {
                'user': user.get_full_name,
                'activate_url': user.confirmation_key,
            }
        }
        send_information_email.delay(**content)


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        re_email = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,30})+$'
        if not re.search(re_email, email):
            return False, _("Entered email address is not valid")
        return True, ''

    @staticmethod
    def validate_captcha(captcha: str, request) -> tuple:
        url = "https://google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.GOOGLE_CAPTCHA_SECRET_KEY,
            'response': captcha,
            'remoteip': get_client_ip(request)
        }
        response = requests.get(url=url, params=params)
        data = response.json()
        status = data.get("success", False)
        return status, data

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @staticmethod
    def make_user_active(user):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return user
