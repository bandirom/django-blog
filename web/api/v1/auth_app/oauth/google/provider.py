from typing import NamedTuple
from urllib.parse import urlencode

import requests
from django.conf import settings

from api.v1.auth_app.oauth.base.exceptions import OAuth2Error
from api.v1.auth_app.oauth.base.factory import provider_registry
from api.v1.auth_app.oauth.base.provider import OAuth2Provider
from auth_app.models import SocialAccountProvider


class GoogleTokenData(NamedTuple):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: str


class GoogleUserInfo(NamedTuple):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str


class GoogleProvider(OAuth2Provider):
    name = SocialAccountProvider.GOOGLE

    def __init__(self):
        super().__init__()
        self.auth_redirect_url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount'
        self.access_token_url = 'https://oauth2.googleapis.com/token'
        self.authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.user_info = 'https://www.googleapis.com/oauth2/v2/userinfo'
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_access_token(self, code: str) -> GoogleTokenData:
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }

        response = requests.post(self.access_token_url, data=data, headers=self.headers)
        if response.status_code != 200:
            raise OAuth2Error()
        return GoogleTokenData(**response.json())

    def get_user_info(self, access_token: str) -> GoogleUserInfo:
        response = requests.get(self.user_info, headers=self.authorization_header(access_token))
        if response.status_code != 200:
            raise OAuth2Error()
        return GoogleUserInfo(**response.json())

    def get_redirect_url(self, request) -> str:
        state = self.setup_state(request)
        data = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
        }
        return f'{self.auth_redirect_url}?{urlencode(data)}'


provider_registry.register(GoogleProvider)
