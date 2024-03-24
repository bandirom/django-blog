from abc import abstractmethod
from typing import TypeVar
from uuid import uuid4

from django.conf import settings

from auth_app.models import SocialAccountProvider


class OAuth2Provider:
    name: SocialAccountProvider = ''

    def __str__(self):
        return self.name

    @property
    def headers(self) -> dict:
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def authorization_header(self, token: str) -> dict:
        return {
            'Authorization': f'Bearer {token}',
        }

    def __init__(self):
        self._name: str = self.name.upper()
        self.config = settings.SOCIAL_ACCOUNTS_PROVIDERS.get(self.name)
        self.enabled = self.config.get('enabled', True)
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']

    @abstractmethod
    def get_access_token(self, code: str):
        pass

    @abstractmethod
    def get_user_info(self, access_token: str):
        pass

    @abstractmethod
    def get_redirect_url(self, request):
        pass

    def setup_state(self, request) -> str:
        state = uuid4().hex
        request.session[self._name] = {}
        request.session[self._name]['state'] = state
        return state

    def validate_state(self, request, expected_state: str) -> bool:
        if self._name not in request.session:
            return False
        if 'state' not in request.session[self._name]:
            return False
        if request.session[self._name]['state'] != expected_state:
            return False
        return True


OAuth2ProviderT = TypeVar('OAuth2ProviderT', bound=OAuth2Provider)
