from datetime import date
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import urlencode, urljoin

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler
from api.v1.auth_app.utils import LoginResponseSerializer, get_client_ip
from main.models import GenderChoice

from main.decorators import except_shell
from main.tasks import send_information_email

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
    birthday: date = None
    gender: GenderChoice = None


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = '/confirm'
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

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class PasswordReset(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
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

    def email_kwargs(self, **kwargs) -> dict:
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        reset_url = self._get_reset_url(uid=uid, token=token)
        return {
            'subject': _('Password Reset'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'reset_url': reset_url,
            },
        }


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


class LoginService:
    response_serializer = LoginResponseSerializer

    error_messages = {
        'not_active': _('Your account is not active. Please contact Your administrator'),
        'wrong_credentials': _('Entered email or password is incorrect'),
    }

    def __init__(self, request):
        self.request = request
        self.rest_settings: dict = settings.REST_AUTH

    def _authenticate(self, **kwargs: str):
        return authenticate(self.request, **kwargs)

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    def validate_user_credentials(self, email: str, password: str) -> User:
        user = self._authenticate(email=email, password=password)
        if not user:
            user = self.get_user(email)
            if not user:
                msg = {'email': self.error_messages['wrong_credentials']}
                raise ValidationError(msg)
            if not user.is_active:
                msg = {'email': self.error_messages['not_active']}
                raise ValidationError(msg)
            msg = {'email': self.error_messages['wrong_credentials']}
            raise ValidationError(msg)
        return user

    def __user_tokens(self, user: User) -> tuple[str, str]:
        refresh: RefreshToken = RefreshToken().for_user(user)
        return refresh.access_token, str(refresh)

    def get_response(self, user: User):
        access_token, refresh_token = self.__user_tokens(user)
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user,
        }
        if return_expiration_times:
            data['access_token_expiration'] = access_token_expiration
            data['refresh_token_expiration'] = refresh_token_expiration
        serializer = self.response_serializer(data)

        response = Response(serializer.data, status=HTTP_200_OK)
        self._set_jwt_cookies(response, access_token, refresh_token)
        return response

    def _set_jwt_cookies(self, response, access_token, refresh_token):
        self._set_jwt_access_cookie(response, access_token)
        self._set_jwt_refresh_cookie(response, refresh_token)

    def __set_jwt_cookie(self, response, key: str, token_value: str, token_expiration) -> None:
        response.set_cookie(
            key=key,
            value=token_value,
            expires=token_expiration,
            secure=self.rest_settings['JWT_AUTH_SECURE'],
            httponly=self.rest_settings['JWT_AUTH_HTTPONLY'],
            samesite=self.rest_settings['JWT_AUTH_SAMESITE'],
            domain=self.rest_settings['JWT_COOKIE_DOMAIN'],
        )

    def _set_jwt_access_cookie(self, response, access_token):
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        self.__set_jwt_cookie(response, self.rest_settings['JWT_AUTH_COOKIE'], access_token, access_token_expiration)

    def _set_jwt_refresh_cookie(self, response, refresh_token):
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        self.__set_jwt_cookie(
            response, self.rest_settings['JWT_AUTH_REFRESH_COOKIE'], refresh_token, refresh_token_expiration
        )


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
        PasswordReset(user).send_email()

    def password_reset_confirm(self, validated_data: dict) -> None:
        data = PasswordResetConfirmData(**validated_data)
        handler = PasswordResetConfirmHandler(token=data.token, uid=data.uid)
        handler.validate()
        user = handler.user
        user.set_password(data.password_1)
        user.save(update_fields=['password'])

    def verify_email_confirm(self, key: str):
        user = User.from_key(key)
        if not user:
            raise ValidationError({'key': _('Invalid or expired confirmation key')})
        if user.is_active:
            raise ValidationError({'key': _('User already verified')})
        user.is_active = True
        user.save(update_fields=['is_active'])

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        user = User.objects.create_user(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password_1,
            is_active=False,
        )
        Profile.objects.create(
            user=user,
            birthday=data.birthday,
            gender=data.gender,
        )
        ConfirmationEmailHandler(user).send_email()


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
