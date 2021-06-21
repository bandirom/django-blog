import logging
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from main.pagination import BasePageNumberPagination
from main.views import TemplateAPIView
from .serializers import CategorySerializer
from .services import BlogService
from . import serializers
from .filters import ArticleFilter

logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination


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
        elif self.action == 'create':
            return serializers.CreateArticleSerializer
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
    pagination_class = BasePageNumberPagination

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'destroy':
            return serializers.UpdateDestroyCommentSerializer
        return serializers.CommentSerializer

    def get_queryset(self):
        return BlogService.get_comments_queryset()

    def get_object(self):
        return BlogService.get_article_comments(article_id=self.kwargs.get('article_id'))

    def list(self, request, article_id):
        queryset = self.filter_queryset(self.get_object())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class NewArticleView(TemplateAPIView):

    def get_queryset(self):
        return BlogService.category_queryset()

    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        data = {
            'categories': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
