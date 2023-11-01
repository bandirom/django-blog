from typing import NamedTuple

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

pytestmark = [pytest.mark.django_db]

User = get_user_model()


class UserTokenUid(NamedTuple):
    uid: str
    token: str


@pytest.fixture
def user_uid_and_token(user: User) -> UserTokenUid:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return UserTokenUid(uid=uid, token=token)
