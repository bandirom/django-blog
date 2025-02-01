from typing import TYPE_CHECKING, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import ValidationError

from api.v1.auth_app.types import PasswordResetDTO

if TYPE_CHECKING:
    from main.models import UserType


User: "UserType" = get_user_model()


class ConfirmationKeyManager:
    def __init__(self):
        self.max_age = settings.EMAIL_CONFIRMATION_EXPIRE_SECONDS

    @staticmethod
    def generate_key(user: User) -> str:
        return signing.dumps(obj=user.pk)

    def get_user_from_key(self, key: str) -> Optional[User]:
        try:
            pk = signing.loads(key, max_age=self.max_age)
            user = User.objects.get(id=pk)
        except (signing.SignatureExpired, signing.BadSignature, User.DoesNotExist):
            user = None
        return user


class PasswordResetManager:
    def __init__(self):
        self.token_generator = default_token_generator

    def generate(self, user: User) -> PasswordResetDTO:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.token_generator.make_token(user)
        return PasswordResetDTO(uid=uid, token=token)

    def validate(self, uid: str, token: str, raise_exception: bool = True) -> User:
        errors = []
        user = self._get_user_by_uid(uid)
        if not user:
            errors.append({'uid': ['Invalid value']})
        if user and not self._validate_token(user, token):
            errors.append({'token': ['Invalid value']})
        if errors and raise_exception:
            raise ValidationError(errors)
        return user

    @staticmethod
    def _get_user_by_uid(uid: str) -> Optional[User]:
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            return User.objects.get(id=uid)
        except (User.DoesNotExist, ValueError):
            return None

    def _validate_token(self, user: User, token: str) -> bool:
        return self.token_generator.check_token(user, token)
