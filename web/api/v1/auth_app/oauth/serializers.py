from rest_framework import serializers

from api.v1.auth_app.oauth.base.factory import provider_registry


class OAuth2RedirectSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=provider_registry.as_choices())
