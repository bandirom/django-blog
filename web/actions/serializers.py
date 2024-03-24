from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Action, LikeDislike

User = get_user_model()


class LikeDislikeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ('vote', 'user', 'date')


class ActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'user', 'action', 'date')


class UserIdFollowQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
