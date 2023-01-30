from django.contrib.auth import get_user_model
from rest_framework import serializers

from actions.choices import FollowIconStatus
from api.v1.actions.services import FollowService

from .choices import GenderChoice
from .models import Profile

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='profile.avatar')
    url = serializers.URLField(source='full_profile_url')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'url')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'birthday',
            'avatar',
            'gender',
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'profile',
            'is_active',
            'phone_number',
            'user_likes',
            'user_posts',
            'followers_count',
            'following_count',
        )
        read_only_fields = ('full_name', 'user_likes', 'user_posts')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update(rep.pop('profile'))
        return rep


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(source='profile.birthday')
    gender = serializers.ChoiceField(source='profile.gender', choices=GenderChoice.choices)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'birthday', 'gender')


class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar')
    follow = serializers.SerializerMethodField('get_follow_status')

    def get_follow_status(self, obj) -> str:
        user = self.context['request'].user
        is_follow = FollowService(user, obj.id).is_user_subscribed()
        return FollowIconStatus.UNFOLLOW if is_follow else FollowIconStatus.FOLLOW

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'follow')
