from rest_framework import serializers

from .services import ExpectedAction, GoogleRecaptcha


class ReCaptchaSerializerMixin(metaclass=serializers.SerializerMetaclass):
    g_recaptcha_response = serializers.CharField(write_only=True)

    def validate_g_recaptcha_response(self, token: str):
        result = GoogleRecaptcha().validate(token, expected_action=ExpectedAction.LOGIN)
        return result
