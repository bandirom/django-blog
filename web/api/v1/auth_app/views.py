from django.conf import settings
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.contrib.auth import logout as django_logout

from . import serializers
from dj_rest_auth import views as auth_views
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from .services import set_jwt_cookies, full_logout


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()

        access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
        refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
        return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)

        data = {
            'user': self.user,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
        }

        if return_expiration_times:
            data['access_token_expiration'] = access_token_expiration
            data['refresh_token_expiration'] = refresh_token_expiration

        serializer = serializer_class(
            instance=data,
            context=self.get_serializer_context(),
        )

        response = Response(serializer.data, status=HTTP_200_OK)
        set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response