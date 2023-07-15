from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from microservice_request.permissions import HasApiKeyOrIsAuthenticated
from . import serializers
from .services import UserDataHandler


class ChatPermissionMixin:
    permission_classes = (HasApiKeyOrIsAuthenticated,)


class JwtUserDataView(ChatPermissionMixin, GenericAPIView):
    serializer_class = serializers.JwtUserDataSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserListByIdView(ChatPermissionMixin, GenericAPIView):
    serializer_class = serializers.UserListByIdSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handler = UserDataHandler()
        user_data: dict = handler.get_user_data(user_ids=serializer.validated_data['user_ids'])
        return Response(user_data)
