from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class JWTLoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    access_token_expiration = serializers.DateTimeField(required=False)
    refresh_token_expiration = serializers.DateTimeField(required=False)
    user = JWTLoginUserSerializer(required=False)
