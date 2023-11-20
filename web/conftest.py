from typing import NamedTuple

import pytest
from django.contrib.auth import get_user_model

from main.models import UserType

pyteststmark = [pytest.mark.django_db]
User: UserType = get_user_model()


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
    return user
