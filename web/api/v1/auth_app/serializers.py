from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.v1.auth_app.services import AuthAppService

from main.models import GenderChoice

User = get_user_model()

error_messages = {
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _('User is already registered with this e-mail address'),
    'password_not_match': _('The two password fields did not match'),
}


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    email = serializers.EmailField()
    password_1 = serializers.CharField(write_only=True, min_length=8)
    password_2 = serializers.CharField(write_only=True, min_length=8)
    birthday = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=GenderChoice.choices, required=False)

    def validate_password1(self, password: str):
        validate_password(password)
        return password

    def validate_email(self, email: str) -> str:
        if AuthAppService.is_user_exist(email):
            raise serializers.ValidationError(_('User is already registered with this e-mail address.'))
        return email

    def validate(self, data: dict):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError({'password_2': error_messages['password_not_match']})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetVerifySerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()


class PasswordResetConfirmSerializer(PasswordResetVerifySerializer):
    password_1 = serializers.CharField(min_length=8, max_length=64)
    password_2 = serializers.CharField(min_length=8, max_length=64)

    def validate_password_1(self, password: str) -> str:
        validate_password(password)
        return password

    def validate(self, data: dict) -> dict:
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError(_('The two password fields did not match.'))
        return data


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
