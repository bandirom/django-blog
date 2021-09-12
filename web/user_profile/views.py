import logging
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from dj_rest_auth.serializers import PasswordChangeSerializer
from .services import UserProfileService
from . import serializers

logger = logging.getLogger(__name__)


class ProfileViewSet(GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'profile':
            return serializers.UserSerializer
        elif self.action == 'image_update':
            return serializers.UserImageSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'update':
            return serializers.UpdateUserProfileSerializer
        return serializers.UserSerializer

    def get_object(self):
        obj = UserProfileService.get_user_profile(self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_template_name(self):
        return 'user_profile/profile.html'

    def profile(self, request):
        serializer = self.get_serializer(instance=self.get_object())
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.template_name = self.get_template_name()
        return response

    def image_update(self, request):
        """
        Change user avatar

        POST request
        """
        serializer = self.get_serializer(data=request.data, instance=request.user.profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def change_password(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})

    def update(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(GenericAPIView):
    serializer_class = serializers.UserListSerializer
    template_name = 'user_profile/user_list.html'

    def get_queryset(self):
        return UserProfileService.user_queryset().exclude(id=self.request.user.id)

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            'user_list': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK, template_name=self.template_name)


class UserProfileByIdView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    template_name = 'user_profile/profile_read_only.html'

    def get_object(self):
        obj = UserProfileService.get_user_profile(self.kwargs.get('user_id'))
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, user_id: int):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK, template_name=self.template_name)


class UserShortInfoView(RetrieveAPIView):
    serializer_class = serializers.UserShortInfoSerializer

    def get_queryset(self):
        return UserProfileService.user_queryset()
