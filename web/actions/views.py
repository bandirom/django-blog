import logging
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework import status
from main.pagination import BasePageNumberPagination

from .services import ActionsService
from . import serializers

logger = logging.getLogger(__name__)


class LikeDislikeView(GenericAPIView):
    serializer_class = serializers.LikeDislikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data: dict = serializer.save()
        return Response(response_data, status.HTTP_200_OK)


class FollowView(GenericAPIView):
    serializer_class = serializers.FollowSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data: dict = serializer.save()
        return Response(response_data, status.HTTP_200_OK)


class UserFollowersView(ListModelMixin, GenericViewSet):
    serializer_class = serializers.UserFollowSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        if self.action == 'user_followers':
            return ActionsService.get_user_followers(self.request.user)
        elif self.action == 'user_following':
            return ActionsService.get_user_following(self.request.user)

    def user_followers(self, request):
        return self.list(request)

    def user_following(self, request):
        return self.list(request)
