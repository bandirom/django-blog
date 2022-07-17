import logging

from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
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


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        self.session_logout()
        response = full_logout(request)
        return response
