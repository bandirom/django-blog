from api.v1.auth_app.oauth.base.provider import OAuth2Provider
from auth_app.models import SocialAccountProvider


class FacebookProvider(OAuth2Provider):
    name = SocialAccountProvider.FACEBOOK
