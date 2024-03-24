from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.auth_app.services import OAuthLoginService

from .provider import GoogleProvider
from .serializers import GoogleLoginSerializer


class GoogleOAuth2CallbackView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = OAuthLoginService(request, GoogleProvider())
        return service.login(code=serializer.data['code'], state=serializer.data['state'])
