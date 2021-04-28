import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from main.pagination import DefaultPagination

from .services import BlogService
from . import serializers
from .filters import ArticleFilter

logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = DefaultPagination


class CategoryViewSet(ViewSet):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return BlogService.category_queryset()


class ArticleViewSet(ViewSet):
    filterset_class = ArticleFilter

    def get_template_name(self):
        if self.action == 'list':
            return 'blog/post_list.html'
        elif self.action == 'retrieve':
            return 'blog/post_detail.html'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ArticleSerializer
        return serializers.FullArticleSerializer

    def get_queryset(self):
        return BlogService.get_active_articles()

    def list(self, request, **kwargs):
        response = super().list(request, **kwargs)
        response.template_name = self.get_template_name()
        return response

    def retrieve(self, request, **kwargs):
        response = super().retrieve(request, **kwargs)
        response.template_name = self.get_template_name()
        return response


class CommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )
    http_method_names = ('get', 'post', 'put', 'delete')

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.UpdateDestroyCommentSerializer
        elif self.action == 'destroy':
            return serializers.UpdateDestroyCommentSerializer
        return serializers.CommentSerializer

    def get_queryset(self):
        return BlogService.get_comments_queryset()

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
