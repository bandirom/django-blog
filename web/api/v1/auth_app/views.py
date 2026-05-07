import hashlib
import json
import logging

from dj_rest_auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .serializers import PasswordResetConfirmSerializer
from .services import AuthAppService, full_logout

logger = logging.getLogger(__name__)

User = get_user_model()

class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        service.create_user(serializer.validated_data)
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )

class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        print(f"PasswordResetView called for email: {email}")
        service = AuthAppService()
        service.send_password_reset_email(email)

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        logger.info("Password reset confirm request received")
        logger.info(f"Request data: {request.data}")

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            logger.info("Serializer is valid, saving...")
            serializer.save()
            logger.info("Password reset successful")
            return Response(
                {
                    'detail': _('Password has been reset with the new password.'),
                    'redirect_url': reverse('auth_app:login')
                },
                status=status.HTTP_200_OK,
            )
        else:
            logger.error(f"Serializer validation errors: {serializer.errors}")
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmPageView(TemplateView):
    template_name = 'auth_app/password_reset_confirm.html'

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Valid token, render the reset form
            return self.render_to_response({
                'uid': uidb64,
                'token': token,
                'validlink': True
            })
        else:
            # Invalid token
            return render(request, 'auth_app/password_reset_invalid.html')


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': _('Email verified')},
            status=status.HTTP_200_OK,
        )
