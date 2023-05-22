from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.utils.translation import get_language

from main.tasks import send_information_email

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class BaseEmailHandler(ABC):
    TEMPLATE_NAME: str = NotImplemented

    def __init__(self, user: Optional[User] = None, language: Optional[str] = None):
        self.user = user
        self._locale: str = language or get_language()

    @property
    def locale(self) -> str:
        return self._locale

    def send_email(self):
        kwargs = self.email_kwargs()
        default_kwargs = {
            'template_name': self.TEMPLATE_NAME,
            'letter_language': self.locale,
        }
        kwargs.update(default_kwargs)
        return send_information_email.apply_async(kwargs=kwargs)

    @abstractmethod
    def email_kwargs(self, **kwargs) -> dict:
        """Provide a dict with at least subject, to_email and context keys"""
