from typing import NamedTuple

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import UserType

pyteststmark = [pytest.mark.django_db]

User: UserType = get_user_model()


class UserToken(NamedTuple):
    access_token: str
    refresh_token: str


@pytest.fixture()
def user() -> User:
    return User.objects.create_user(
        email='harley.quinn@email.com',
        password='some_p@ssword',
        first_name='Margot',
        last_name='Robbie',
    )


@pytest.fixture()
def user_tokens(user) -> UserToken:
    refresh: RefreshToken = RefreshToken().for_user(user)
    return UserToken(access_token=refresh.access_token, refresh_token=str(refresh))


@pytest.fixture()
def api_client(client: Client, user_tokens) -> Client:
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_tokens.access_token}'
    return client
