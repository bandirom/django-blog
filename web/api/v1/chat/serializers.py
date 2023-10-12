from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UserListByIdSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField(min_value=1))


class UserShortInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source='avatar_url')

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'avatar',
        )


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
        return UserShortInfoSerializer(self.user, context=self.context).data
