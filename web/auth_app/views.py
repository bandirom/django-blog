import logging
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _

from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import (
    VerifyEmailView as _VerifyEmailView,
)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from . import serializers
from .services import full_logout, AuthAppService

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        user = confirmation.email_address.user
        AuthAppService.make_user_active(user)
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=HTTP_200_OK)


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response
