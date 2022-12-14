from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from user_profile.models import Profile

User = get_user_model()


class UserChatListSerializer(serializers.Serializer):
    user_ids = serializers.ListSerializer(child=serializers.IntegerField(min_value=1))


class UserShortInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source='avatar_url')
    # url = serializers.URLField(source='get_absolute_url')

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
            self.user = User.objects.select_related('profile').get(pk=access_token['user_id'])
        except (TokenError, User.DoesNotExist) as e:
            raise serializers.ValidationError(e)
        return jwt

    @property
    def data(self) -> dict:
        return UserShortInfoSerializer(self.user, context=self.context).data


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar',)

    def validate_avatar(self, avatar):
        if avatar.size > settings.USER_AVATAR_MAX_SIZE * 1024 * 1024:
            raise serializers.ValidationError(
                _("Max size is {size} MB".format(size=settings.USER_AVATAR_MAX_SIZE))
            )
        return avatar

    def save(self):
        if self.instance.avatar and not self.instance.is_default_image():
            self.instance.set_image_to_default()
        self.instance.avatar = self.validated_data['avatar']
        return self.instance.save(update_fields=['avatar'])
