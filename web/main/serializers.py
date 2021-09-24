from urllib.parse import urljoin

import pytz
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers

User = get_user_model()


class SetTimeZoneSerializer(serializers.Serializer):
    timezone = serializers.ChoiceField(choices=pytz.common_timezones)


class JwtUserDataSerializer(serializers.Serializer):
    jwt = serializers.CharField()

    def validate_jwt(self, jwt: str):
        try:
            access_token = AccessToken(jwt)
            self.user = User.objects.get(pk=access_token['user_id'])
        except (TokenError, User.DoesNotExist) as e:
            raise serializers.ValidationError(e)
        return jwt

    @property
    def data(self) -> dict:
        if not self.user:
            return {}
        return {
            'id': self.user.id,
            'full_name': self.user.full_name(),
            'avatar': urljoin(settings.BACKEND_SITE, self.user.profile.avatar.url),
        }
