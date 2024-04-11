from typing import TYPE_CHECKING
from urllib.parse import quote, urlencode, urljoin

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_service.password_reset import PasswordResetService
from api.email_service.sign_up import SignUpEmailService
from api.v1.auth_app.oauth.base.provider import OAuth2Provider
from api.v1.auth_app.oauth.google.provider import GoogleTokenData, GoogleUserInfo
from api.v1.auth_app.utils import LoginResponseSerializer, get_client_ip
from auth_app.models import SocialAccount

from .managers import ConfirmationKeyManager, PasswordResetManager
from .oauth.base.exceptions import OAuth2Error
from .types import CreateUserData, PasswordResetConfirmData
from main.decorators import except_shell

if TYPE_CHECKING:
    from django.http import HttpResponse

    from main.models import UserType

User: 'UserType' = get_user_model()


class PasswordResetHandler:
    def __init__(self, email: dict):
        self.email = email
        self.frontend_url = settings.FRONTEND_URL
        self.frontend_path = '/reset/confirm'

    def reset_password(self):
        user = User.objects.get(email=self.email)
        reset_url = self._get_reset_url(user)
        PasswordResetService(user).send_email(reset_url=reset_url)

    def _get_reset_url(self, user) -> str:
        values = PasswordResetManager().generate(user)
        url = urljoin(self.frontend_url, self.frontend_path)
        reset_url = f'{url}?uid={values.uid}&token={values.token}'
        return quote(reset_url, safe=':/?&=')


class SignUpHandler:
    def __init__(self, validated_data: dict):
        self.data = CreateUserData(**validated_data)
        self.frontend_url = settings.FRONTEND_URL
        self.frontend_path = '/confirm'

    @transaction.atomic()
    def create_user(self):
        user = User.objects.create_user(
            email=self.data.email,
            first_name=self.data.first_name,
            last_name=self.data.last_name,
            password=self.data.password_1,
            birthday=self.data.birthday,
            gender=self.data.gender,
            is_active=False,
        )
        activate_url = self._get_activate_url(user)
        SignUpEmailService(user).send_email(activate_url=activate_url)

    def _get_activate_url(self, user) -> str:
        url = urljoin(self.frontend_url, self.frontend_path)
        query_params: str = urlencode(
            {
                'key': ConfirmationKeyManager.generate_key(user),
            },
            safe=':+',
        )
        return f'{url}?{query_params}'


class LoginService:
    response_serializer = LoginResponseSerializer

    error_messages = {
        'not_active': _('Your account is not active. Please contact Your administrator'),
        'wrong_credentials': _('Entered email or password is incorrect'),
    }

    def __init__(self, request):
        self.request = request
        self.settings: dict = settings.REST_AUTH

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
            secure=self.settings['JWT_AUTH_SECURE'],
            httponly=self.settings['JWT_AUTH_HTTPONLY'],
            samesite=self.settings['JWT_AUTH_SAMESITE'],
            domain=self.settings['JWT_COOKIE_DOMAIN'],
        )

    def _set_jwt_access_cookie(self, response: "HttpResponse", access_token: str):
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        self.__set_jwt_cookie(response, self.settings['JWT_AUTH_COOKIE'], access_token, access_token_expiration)

    def _set_jwt_refresh_cookie(self, response: "HttpResponse", refresh_token: str):
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        self.__set_jwt_cookie(
            response, self.settings['JWT_AUTH_REFRESH_COOKIE'], refresh_token, refresh_token_expiration
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

    @staticmethod
    def password_reset_confirm(validated_data: dict) -> None:
        data = PasswordResetConfirmData(**validated_data)
        manager = PasswordResetManager()
        user = manager.validate(token=data.token, uid=data.uid)
        user.set_password(data.password_1)
        user.save(update_fields=['password'])

    @staticmethod
    def verify_email_confirm(key: str) -> User:
        user = ConfirmationKeyManager().get_user_from_key(key)
        if not user:
            raise ValidationError({'key': _('Invalid or expired confirmation key')})
        if user.is_active:
            raise ValidationError({'key': _('User already verified')})
        user.is_active = True
        user.save(update_fields=['is_active'])
        return user


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


class OAuthLoginService:
    def __init__(self, request, provider: OAuth2Provider):
        self.request = request
        self.provider = provider

    def create_social_account(self, user: User, uid: str):
        return SocialAccount.objects.create(
            user=user,
            provider=self.provider.name,
            uid=uid,
        )

    @staticmethod
    def get_user_avatar(url: str) -> ContentFile:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return ContentFile(response.content, name='google_image.png')

    @transaction.atomic()
    def get_or_create_user(self, user_data: GoogleUserInfo) -> User:
        if user := User.objects.filter(Q(social_accounts__uid=user_data.id) & Q(email=user_data.email)).first():
            return user
        if user := User.objects.filter(email=user_data.email).first():
            self.create_social_account(user, user_data.id)
            return user
        user = User.objects.create_user(
            email=user_data.email,
            password=None,
            first_name=user_data.given_name,
            last_name=user_data.family_name,
            avatar=self.get_user_avatar(user_data.picture),
            is_active=user_data.verified_email,
        )
        self.create_social_account(user, user_data.id)
        return user

    def login(self, code: str, state: str):
        if not self.provider.validate_state(self.request, state):
            raise OAuth2Error('Invalid state')

        response_data: GoogleTokenData = self.provider.get_access_token(code)

        user_data: GoogleUserInfo = self.provider.get_user_info(response_data.access_token)

        user = self.get_or_create_user(user_data)
        login_service = LoginService(self.request)
        return login_service.get_response(user)
