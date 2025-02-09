from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

from api.v1.auth_app.managers import PasswordResetManager
from api.v1.auth_app.types import PasswordResetDTO

if TYPE_CHECKING:
    from main.models import UserType


User: "UserType" = get_user_model()


@pytest.fixture
def user_uid_and_token(user: User) -> PasswordResetDTO:
    manager = PasswordResetManager()
    return manager.generate(user)


@pytest.fixture()
def inactive_user(user) -> User:
    user.is_active = False
    user.save(update_fields=["is_active"])
    return user
