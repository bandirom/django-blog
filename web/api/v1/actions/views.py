from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from actions.models import Action

from ..profile.services import UserQueryService
from . import serializers
from .services import FollowService, LikeService
from main.pagination import BasePageNumberPagination

swagger_tags = ['Like']


class LikeDislikeView(GenericAPIView):
    serializer_class = serializers.LikeDislikeSerializer

    # @swagger_auto_schema(tags=swagger_tags)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LikeService(
            user=request.user,
            vote=serializer.validated_data['vote'],
            model=serializer.validated_data['model'],
            object_id=serializer.validated_data['object_id'],
        )

        response_data: dict = service.make_like()
        return Response(response_data, status.HTTP_200_OK)


class FollowView(GenericAPIView):
    serializer_class = serializers.FollowSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = FollowService(user=request.user, user_id=serializer.data['user_id'])
        follow_status = service.subscribe()
        return Response({'status': follow_status}, status.HTTP_200_OK)


class UserFollowersView(ListModelMixin, GenericViewSet):
    serializer_class = serializers.UserFollowSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        service = UserQueryService()
        if self.action == 'user_followers':
            return service.get_user_followers(self.request.user)
        elif self.action == 'user_following':
            return service.get_user_following(self.request.user)
        elif self.action == 'user_followers_by_id':
            user = service.get_simple_user(self.kwargs['user_id'])
            return service.get_user_followers(user)
        elif self.action == 'user_following_by_id':
            user = service.get_simple_user(self.kwargs['user_id'])
            return service.get_user_following(user)

    def user_followers(self, request):
        return self.list(request)

    def user_following(self, request):
        return self.list(request)

    def user_followers_by_id(self, request, user_id: int):
        return self.list(request)

    def user_following_by_id(self, request, user_id: int):
        return self.list(request)


class FeedView(ListAPIView):
    serializer_class = serializers.FeedListSerializer

    def get_queryset(self):
        return Action.objects.filter(user=self.request.user)
