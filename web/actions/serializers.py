from django.contrib.auth import get_user_model
from rest_framework import serializers

from .choices import FollowIconStatus
from .models import Action, LikeDislike
from .services import ActionsService

User = get_user_model()


class LikeDislikeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ('vote', 'user', 'date')


class UserFollowSerializer(serializers.ModelSerializer):
    """For list of user following and followers"""

    profile_url = serializers.URLField(source='get_absolute_url')
    avatar = serializers.ImageField(source='profile.avatar')

    follow = serializers.SerializerMethodField('get_follow_status')

    def get_follow_status(self, obj) -> str:
        user = self.context['request'].user
        if user == obj:
            return None
        is_follow = ActionsService.is_user_followed(user, obj.id)
        return FollowIconStatus.UNFOLLOW if is_follow else FollowIconStatus.FOLLOW

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'profile_url', 'follow')


class ActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'user', 'action', 'date')


class UserIdFollowQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
