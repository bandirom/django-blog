from rest_framework import serializers

from .services import validate_recaptcha


class ReCaptchaMixin(metaclass=serializers.SerializerMetaclass):
    g_recaptcha_response = serializers.CharField(write_only=True)

    def validate_g_recaptcha_response(self, token: str):
        result = validate_recaptcha(token)

        if (result['success']):
            return token
        else:
            raise serializers.ValidationError({'recaptcha': result['error-codes']}, code='wrong_recaptcha')
