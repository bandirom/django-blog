from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    confirmation_key = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

### TODO: заменить на класс
    def set_confirmation_key(self):
        """Устанавливает ключ подтверждения"""
        self.confirmation_key = signing.dumps(self.pk)
        return self.confirmation_key

    def generate_password_reset_token(self) -> str:
        """Генерирует токен для сброса пароля"""
        return signing.dumps({
            'user_id': self.pk,
            'timestamp': timezone.now().timestamp()
        })

    def verify_confirmation_key(self, key: str) -> bool:
        """Проверяет ключ подтверждения"""
        try:
            user_id = signing.loads(key)
            return user_id == self.pk
        except (signing.BadSignature, KeyError):
            return False

    def verify_password_reset_token(self, token: str) -> bool:
        """Проверяет токен сброса пароля"""
        try:
            data = signing.loads(token)
            return data.get('user_id') == self.pk
        except (signing.BadSignature, KeyError, TypeError):
            return False
