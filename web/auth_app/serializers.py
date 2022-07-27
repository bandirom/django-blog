from dj_rest_auth import serializers as auth_serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user_profile.choices import GenderChoice

from .forms import PassResetForm
from .services import AuthAppService

User = get_user_model()

error_messages = {
    'not_verified': _('Email not verified'),
    'not_active': _('Your account is not active. Please contact Your administrator'),
    'wrong_credentials': _('Entered email or password is incorrect'),
    'already_registered': _("User is already registered with this e-mail address"),
    'password_not_match': _("The two password fields didn't match"),
}


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    birthday = serializers.DateField(required=False, source='profile.birthday')
    gender = serializers.ChoiceField(choices=GenderChoice.choices, required=False, source='profile.gender')

    def validate_password1(self, password: str):
        validate_password(password)
        return password

    def validate_email(self, email: str) -> str:
        # if "email_address_exists(email)":
        #     raise serializers.ValidationError(_("User is already registered with this e-mail address."))
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': error_messages['password_not_match']})
        return data

    def save(self, **kwargs):
        profile_data: dict = self.validated_data.pop('profile')
        self.validated_data['password'] = self.validated_data.pop('password1')
        del self.validated_data['password2']
        self.validated_data.pop('captcha', None)
        user = User.objects.create_user(**self.validated_data, is_active=False)
        user.profile.birthday = profile_data.get('birthday')
        user.profile.gender = profile_data.get('gender')
        user.profile.save()
        # CeleryService.send_email_confirm(user)
        return user



class UserSignUpWithCaptchaSerializer(UserSignUpSerializer):
    pass



class PasswordResetSerializer(auth_serializers.PasswordResetSerializer):
    password_reset_form_class = PassResetForm


class PasswordResetConfirmSerializer(auth_serializers.PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(max_length=128, min_length=8)
    new_password2 = serializers.CharField(max_length=128, min_length=8)


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
