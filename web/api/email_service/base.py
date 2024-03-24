from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, TypedDict

from django.contrib.auth import get_user_model
from django.utils.translation import get_language

from main.tasks import send_information_email

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class EmailSendData(TypedDict):
    subject: str
    template_name: str
    language: str
    to_email: str
    context: dict
    from_email: Optional[str]
    file_path_attachments: Optional[str]


class BaseEmailService(ABC):
    def __init__(self, user: Optional[User] = None, language: Optional[str] = None, from_email: Optional[str] = None):
        self._user = user
        self._locale: str = language or get_language()
        self.from_email = from_email

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def user(self) -> User:
        assert self._user, 'User object were not provided'
        return self._user

    @property
    @abstractmethod
    def template_name(self) -> str:
        """Template email path"""

    @property
    def to_email(self) -> str:
        return self.user.email

    def email_context(self, **kwargs) -> dict:
        """Provide dict with data for email template rendering"""
        return {}

    @property
    @abstractmethod
    def email_subject(self) -> str:
        """Provide email subject"""

    def get_email_data(self, **kwargs) -> EmailSendData:
        return {
            'subject': self.email_subject,
            'template_name': self.template_name,
            'language': self.locale,
            'to_email': self.to_email,
            'context': self.email_context(**kwargs),
            'from_email': self.from_email,
            'file_path_attachments': None,
        }

    def send_email(self, **kwargs):
        kwargs: dict = self.get_email_data(**kwargs)
        return send_information_email.apply_async(kwargs=kwargs)
