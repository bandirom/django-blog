import logging

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v1.profile.serializers import UserShortInfoSerializer
from api.v1.profile.services import UserQueryService

from . import serializers

logger = logging.getLogger(__name__)


class ProfileViewSet(GenericViewSet):
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get_serializer_class(self):
        if self.action == 'profile':
            return serializers.UserSerializer
        elif self.action == 'update':
            return serializers.UpdateUserProfileSerializer
        return serializers.UserSerializer

    def get_object(self):
        obj = UserQueryService.get_user_by_id(self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    @property
    def template_name(self):
        return 'user_profile/profile.html'

    def profile(self, request):
        serializer = self.get_serializer(instance=self.get_object())
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def update(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileByIdView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    template_name = 'user_profile/profile_read_only.html'
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get_object(self):
        obj = UserQueryService.get_user_by_id(self.kwargs.get('user_id'))
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, user_id: int):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK, template_name=self.template_name)


class UserShortInfoView(RetrieveAPIView):
    serializer_class = UserShortInfoSerializer

    def get_queryset(self):
        return UserQueryService.get_queryset()
