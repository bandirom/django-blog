from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from rest_framework import serializers

from actions.choices import FollowIconStatus, LikeObjChoice, LikeStatus
from api.v1.actions.services import FollowService

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class LikeDislikeSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    model = serializers.ChoiceField(choices=LikeObjChoice.choices)
    vote = serializers.ChoiceField(choices=LikeStatus.choices)


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class UserFollowSerializer(serializers.ModelSerializer):
    """For list of user following and followers"""

    profile_url = serializers.URLField(source='get_absolute_url')

    follow = serializers.SerializerMethodField('get_follow_status')

    def get_follow_status(self, obj) -> Optional[FollowIconStatus]:
        user = self.context['request'].user
        if user == obj:
            return None
        is_follow = FollowService(user=user, user_id=obj.id).is_user_subscribed()
        return FollowIconStatus.UNFOLLOW if is_follow else FollowIconStatus.FOLLOW

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'profile_url', 'follow')
