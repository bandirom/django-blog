from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_profile.serializers import ProfileSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'profile', 'is_active', 'email_verified')
        read_only_fields = ('full_name', 'email_verified')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update(rep.pop('profile'))
        return rep
