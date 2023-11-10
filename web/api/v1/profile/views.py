from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .services import UserQueryService


class AvatarUpdateView(GenericAPIView):
    serializer_class = serializers.AvatarUpdateSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': True})


class CurrentUserView(GenericAPIView):
    service = UserQueryService

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    def get_queryset(self):
        service = self.service()
        if self.request.method == 'PUT':
            return service.get_queryset()
        return service.user_profile_queryset()

    def get_object(self):
        service = self.service()
        return service.get_user_profile(user_id=self.request.user.id)

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_serializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListView(ListAPIView):
    serializer_class = serializers.UserListSerializer

    def get_queryset(self):
        return UserQueryService.get_queryset(is_active=True)
