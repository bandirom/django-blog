import re
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler
from main.decorators import except_shell

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'http://localhost:8008')
    FRONTEND_PATH = 'auth/confirm'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        """Формирует полный URL для подтверждения"""
        if settings.DEBUG:
            # Используем localhost для разработки
            base_url = "http://localhost:8008"
        else:
            base_url = self.FRONTEND_URL.rstrip('/')

        path = self.FRONTEND_PATH.lstrip('/')

        query_params = urlencode({
            'key': self.user.confirmation_key,
            'email': self.user.email,
        })

        full_url = f"{base_url}/{path}?{query_params}"
        return full_url

    def email_kwargs(self, **kwargs) -> dict:
        activate_url = self._get_activate_url()

        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': activate_url,
                'message': f"Please click the link to confirm your registration: {activate_url}",
                'expiry_hours': 24
            },
        }


class PasswordResetEmailHandler:
    FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'http://localhost:8008')

    def __init__(self, user, token):
        self.user = user
        self.token = token
        self._cached_url = None

    def _get_password_reset_url(self) -> str:
        """Формирует полный URL для подтверждения"""
        if self._cached_url:
            return self._cached_url

        if settings.DEBUG:
            # Используем localhost для разработки
            base_url = "http://localhost:8008"
        else:
            base_url = self.FRONTEND_URL.rstrip('/')

        reset_url = reverse('api:v1:auth_app:password-reset-confirm', kwargs={
            'token': self.token
        })

        full_url = f"{base_url}{reset_url}"
        return full_url

    def send_email(self, subject=None, message=None, recipient_list=None):
        full_reset_url = self._get_password_reset_url()

        subject = subject or "Password Reset Request"
        message = message or f"""
        Hello {self.user.first_name or self.user.email},

        You requested a password reset. Click the link below to reset your password:

        {full_reset_url}

        If you didn't request this, please ignore this email.

        This link will expire in 24 hours.
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list or [self.user.email],
            fail_silently=False,
        )

class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        pattern = re.compile(r'[@.]')
        username = pattern.sub('_', data.email)
        user = User.objects.create_user(
            # username=username,
            email=data.email,
            password=data.password_1,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=False,
        )
        self.send_confirmation_email(user)
        return None

    def send_confirmation_email(self, user: User):
        # Сохраняем confirmation_key в модели пользователя
        user.confirmation_key = signing.dumps(user.id)
        user.save(update_fields=['confirmation_key'])

        handler = ConfirmationEmailHandler(user=user)

        handler.send_email(
            subject=None,
            message=None,
            recipient_list=[user.email]
        )

    def send_password_reset_email(self, email: str):
        """Отправляет email со ссылкой для сброса пароля"""
        try:
            user = self.get_user(email)
        except User.DoesNotExist:
            # Не раскрываем, существует ли пользователь (безопасность)
            return None

        token = user.generate_password_reset_token()

        # Отправляем email
        handler = PasswordResetEmailHandler(user=user, token=token)
        handler.send_email(
            subject=None,
            message=None,
            recipient_list=[user.email]
        )
        return None

def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    auth_cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
    refresh_cookie_name = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']

    response.delete_cookie(auth_cookie_name)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        response.data = {"detail": _("Refresh token was not included in request data.")}
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except (TokenError, AttributeError, TypeError) as error:
        if hasattr(error, 'args'):
            if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                response.data = {"detail": _(error.args[0])}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response.data = {"detail": _("An error has occurred.")}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response
