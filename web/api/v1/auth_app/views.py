from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .managers import PasswordResetManager
from .services import AuthAppService, LoginService, PasswordResetHandler, SignUpHandler, LogoutService


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = SignUpHandler(serializer.validated_data)
        service.create_user()
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        service = LoginService(request)
        user = service.validate_user_credentials(email=data['email'], password=data['password'])
        return service.get_response(user)


class LogoutView(APIView):
    def post(self, request):
        service = LogoutService(request)
        return service.logout()


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = PasswordResetHandler(serializer.data['email'])
        service.reset_password()
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetVerifyView(GenericAPIView):
    serializer_class = serializers.PasswordResetVerifySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handler = PasswordResetManager()
        handler.validate(
            token=serializer.validated_data['token'],
            uid=serializer.validated_data['uid'],
            raise_exception=True,
        )
        return Response({'detail': True}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthAppService.password_reset_confirm(serializer.validated_data)
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthAppService.verify_email_confirm(key=serializer.data['key'])
        return Response(
            {'detail': _('Email verified')},
            status=status.HTTP_200_OK,
        )
