from base64 import b64decode
from typing import NamedTuple

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from user_profile.models import Profile

from main.models import UserType

pyteststmark = [pytest.mark.django_db]

User: UserType = get_user_model()

raw_image: str = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA'
    'AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII='
)


@pytest.fixture()
def image_content_file() -> ContentFile:
    _format, _raw_image = raw_image.split(';base64,')
    ext = _format.split('/')[-1]
    return ContentFile(b64decode(_raw_image), name=f'image.{ext}')


class UserToken(NamedTuple):
    access_token: str
    refresh_token: str


@pytest.fixture()
def user() -> User:
    user = User.objects.create_user(
        email='harley.quinn@email.com',
        password='some_p@ssword',
        first_name='Margot',
        last_name='Robbie',
    )
    Profile.objects.create(user=user)
    return user


@pytest.fixture()
def user_tokens(user) -> UserToken:
    refresh: RefreshToken = RefreshToken().for_user(user)
    return UserToken(access_token=refresh.access_token, refresh_token=str(refresh))


@pytest.fixture()
def api_client(client: Client, user_tokens) -> Client:
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_tokens.access_token}'
    # client.cookies
    return client
