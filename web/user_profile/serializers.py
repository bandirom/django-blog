from django.contrib.auth import get_user_model
from rest_framework import serializers

from actions.choices import FollowIconStatus
from api.v1.actions.services import FollowService

from main.models import GenderChoice

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='full_profile_url')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'url')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'phone_number',
            'user_likes',
            'user_posts',
            'followers_count',
            'following_count',
            'avatar',
        )
        read_only_fields = ('full_name', 'user_likes', 'user_posts')


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=GenderChoice.choices)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthday', 'gender')


class UserListSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField('get_follow_status')

    def get_follow_status(self, obj) -> str:
        user = self.context['request'].user
        is_follow = FollowService(user, obj.id).is_user_subscribed()
        return FollowIconStatus.UNFOLLOW if is_follow else FollowIconStatus.FOLLOW

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'follow')
