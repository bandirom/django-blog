from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


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


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)

    def validate_avatar(self, avatar):
        if avatar.size > settings.USER_AVATAR_MAX_SIZE * 1024 * 1024:
            raise serializers.ValidationError(_("Max size is {size} MB".format(size=settings.USER_AVATAR_MAX_SIZE)))
        return avatar

    def save(self):
        if self.instance.avatar and not self.instance.is_default_image():
            self.instance.set_image_to_default()
        self.instance.avatar = self.validated_data['avatar']
        return self.instance.save(update_fields=['avatar'])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8)

    def validate_new_password_1(self, password: str) -> str:
        validate_password(password)
        return password

    def validate(self, data: dict) -> dict:
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(_('The two password fields did not match.'))
        return data

    def update(self, instance: User, validated_data: dict):
        instance.set_password(validated_data['new_password1'])
        instance.save(update_fields=['password'])
        return instance
