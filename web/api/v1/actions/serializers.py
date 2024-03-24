from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from rest_framework import serializers

from actions.choices import FollowStatus, LikeObjChoice, LikeStatus
from actions.models import Action
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
    profile_url = serializers.URLField(source='get_absolute_url')

    follow = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'profile_url', 'follow')


class UserFeedSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source='avatar_url')

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'avatar',
        )


class FeedListSerializer(serializers.ModelSerializer):
    user = UserFeedSerializer()

    class Meta:
        model = Action
        fields = ('id', 'user', 'action', 'date')
