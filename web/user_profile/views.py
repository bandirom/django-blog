import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from .services import UserProfileService
from . import serializers

logger = logging.getLogger(__name__)


class ProfileViewSet(GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'profile':
            return serializers.UserSerializer
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
