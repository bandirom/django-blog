from rest_framework import serializers


class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()
    scope = serializers.CharField()
