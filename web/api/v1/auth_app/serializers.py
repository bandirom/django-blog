import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.v1.auth_app.services import AuthAppService

logger = logging.getLogger(__name__)


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

    def validate_password_1(self, password: str):
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

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, data: dict):
        email = data.get('email')
        password = data.get('password')
        user = self.authenticate(email=email, password=password)
        if not user:
            user = AuthAppService.get_user(email)
            if not user:
                msg = {'email': error_messages['wrong_credentials']}
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = {'email': error_messages['not_active']}
                raise serializers.ValidationError(msg)
            msg = {'email': error_messages['wrong_credentials']}
            raise serializers.ValidationError(msg)
        data['user'] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            self.user = user
        except User.DoesNotExist as err:
            raise serializers.ValidationError("No user found with this email") from None
        return value

    ### TODO: Удалить метод save
    def save(self, request):
        if not hasattr(self, 'user'):
            return

        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        reset_path = reverse('api:v1:auth_app:password-reset-confirm-page', kwargs={
            'uidb64': uid,
            'token': token
        })
        reset_url = request.build_absolute_uri(reset_path)

        send_mail(
            subject='Password Reset Request',
            message=f'Click this link to reset your password: {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    password_1 = serializers.CharField(min_length=8, max_length=64)
    password_2 = serializers.CharField(min_length=8, max_length=64)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        logger.info(f"Validating password reset: uid={attrs.get('uid')}, token={attrs.get('token')[:10]}...")

        # Check passwords match
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError({"password_2": "Passwords do not match."})

        # Decode uid and get user
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            logger.info(f"Decoded uid: {uid}")
            user = User.objects.get(pk=uid)
            attrs['user'] = user
            logger.info(f"User found: {user.email}")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logger.error(f"Failed to decode uid or get user: {e}")
            raise serializers.ValidationError({"uid": "Invalid user ID."}) from None

        # Check token
        if not default_token_generator.check_token(user, attrs['token']):
            logger.warning(f"Invalid or expired token for user {user.email}")
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        logger.info(f"Token validation successful for user {user.email}")
        return attrs

    def save(self):
        """Set new password"""
        user = self.validated_data['user']
        new_password = self.validated_data['password_1']
        logger.info(f"Setting new password for user {user.email}")
        user.set_password(new_password)
        user.save()
        logger.info(f"Password successfully reset for user {user.email}")
        return user

class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
