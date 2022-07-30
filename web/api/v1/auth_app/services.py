from urllib.parse import urljoin, urlencode

import requests
from dj_rest_auth.jwt_auth import set_jwt_refresh_cookie
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from auth_app.utils import get_client_ip
from main.decorators import except_shell
from main.tasks import send_information_email
from typing import TYPE_CHECKING, NamedTuple


if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class PasswordResetConfirmData(NamedTuple):
    uid: str
    token: str
    password_1: str
    password_2: str


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class BaseEmailHandler:
    FRONTEND_PATH = ''
    FRONTEND_URL = settings.FRONTEND_URL
    TEMPLATE_NAME = ''

    def __init__(self, user: User, language: str = 'en'):
        self.user = user
        self._locale: str = language if not language else get_language()

    @property
    def locale(self) -> str:
        return self._locale


class Confirmation(BaseEmailHandler):
    FRONTEND_PATH = '/confirm/'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def send_confirmation_email(self):
        kwargs = {
            'subject': _('Register confirmation email'),
            'template_name': self.TEMPLATE_NAME,
            'to_email': self.user.email,
            'letter_language': self.locale,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }
        send_information_email.apply_async(kwargs=kwargs)


class PasswordReset(BaseEmailHandler):
    TEMPLATE_NAME = 'emails/password_reset.html'
    FRONTEND_PATH = '/reset/confirm'

    def _get_reset_url(self, uid: str, token: str) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'uid': uid,
                'token': token,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def send_password_reset_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        reset_url = self._get_reset_url(uid=uid, token=token)
        kwargs = {
            'subject': _('Password Reset'),
            'template_name': self.TEMPLATE_NAME,
            'to_email': self.user.email,
            'letter_language': self.locale,
            'context': {
                'user': self.user.full_name,
                'reset_url': reset_url,
            },
        }
        send_information_email.apply_async(kwargs=kwargs)


from django.utils.http import urlsafe_base64_decode


class PasswordResetConfirmHandler:
    def __init__(self, *, uid: str, token: str):
        self._token = token
        self._uid = uid
        self._user = None

    @property
    def user(self) -> User:
        return self._user

    def validate(self):
        self._user = self._get_user_by_uid_or_exception(self._uid)
        self._validate_token()

    @staticmethod
    def _get_user_by_uid_or_exception(uid: str) -> User:
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            return User.objects.get(id=uid)
        except (
            User.DoesNotExist,
            OverflowError,
            TypeError,
            ValueError,
        ):
            raise ValidationError({'uid': ['Invalid value']})

    def _validate_token(self):
        if not default_token_generator.check_token(self.user, self._token):
            raise ValidationError({'token': ['Invalid value']})


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def validate_captcha(captcha: str, request) -> tuple:
        url = "https://google.com/recaptcha/api/siteverify"
        params = {
            'secret': settings.GOOGLE_CAPTCHA_SECRET_KEY,
            'response': captcha,
            'remoteip': get_client_ip(request),
        }
        response = requests.get(url=url, params=params)
        data = response.json()
        _status = data.get("success", False)
        return _status, data

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    def password_reset(self, email: str) -> None:
        user = self.get_user(email)
        if not user:
            return
        PasswordReset(user).send_password_reset_email()

    def password_reset_confirm(self, validated_data: dict) -> None:
        data = PasswordResetConfirmData(**validated_data)
        handler = PasswordResetConfirmHandler(token=data.token, uid=data.uid)
        handler.validate()
        user = handler.user
        user.set_password(data.password_1)
        user.save(update_fields=['password'])

    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        print(f'{data=}')


def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    if cookie_name := getattr(settings, 'JWT_AUTH_COOKIE', None):
        response.delete_cookie(cookie_name)
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        # add refresh token to blacklist
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


def set_jwt_access_cookie(response, access_token):
    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
    cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
    cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
    cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')

    if cookie_name:
        response.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            domain=getattr(settings, 'JWT_COOKIE_DOMAIN', None),
        )


def set_jwt_cookies(response, access_token, refresh_token):
    set_jwt_access_cookie(response, access_token)
    set_jwt_refresh_cookie(response, refresh_token)
