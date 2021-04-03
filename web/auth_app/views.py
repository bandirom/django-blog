import logging
from django.contrib.auth import logout as django_logout

from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import (
    VerifyEmailView as _VerifyEmailView,
)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from . import serializers
from .services import full_logout

logger = logging.getLogger(__name__)


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer


class PasswordResetView(auth_views.PasswordResetView):
    serializer_class = serializers.PasswordResetSerializer


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    serializer_class = serializers.PasswordResetConfirmSerializer


class VerifyEmailView(_VerifyEmailView):

    def get_serializer(self, *args, **kwargs):
        return serializers.VerifyEmailSerializer(*args, **kwargs)


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        # self.session_logout()
        response = full_logout(request)
        return response
