from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserListByIdSerializer(serializers.Serializer):

    user_ids = serializers.ListField(child=serializers.IntegerField(min_value=1))


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
