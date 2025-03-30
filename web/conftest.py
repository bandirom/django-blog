from base64 import b64decode

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import SimpleCookie
from django.test import Client, override_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.auth_app.services import AuthToken

from main.models import UserType

pytestmark = [pytest.mark.django_db]

User: UserType = get_user_model()

raw_image: str = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA'
    'AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII='
)

celery_runtime_tasks = override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
)


@pytest.fixture()
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(';base64,')
    ext = _format.split('/')[-1]
    return ContentFile(b64decode(_raw_image), name=f'image.{ext}')


@pytest.fixture()
def user() -> User:
    user = User.objects.create_user(
        email='harley.quinn@email.com',
        password='some_p@ssword',
        first_name='Margot',
        last_name='Robbie',
    )
    return user


@pytest.fixture()
def user_tokens(user) -> AuthToken:
    refresh: RefreshToken = RefreshToken().for_user(user)
    return AuthToken(access_token=str(refresh.access_token), refresh_token=str(refresh))


@pytest.fixture()
def jwt_cookies(user_tokens: AuthToken) -> SimpleCookie:
    return SimpleCookie(
        {
            settings.REST_AUTH["JWT_AUTH_COOKIE"]: user_tokens.access_token,
            settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]: user_tokens.refresh_token,
        }
    )


@pytest.fixture()
def api_client(client: Client, jwt_cookies) -> Client:
    # client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_tokens.access_token}'
    client.cookies = jwt_cookies
    return client
