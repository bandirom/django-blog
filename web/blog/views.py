import logging
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from api.v1.blog import serializers
from api.v1.blog.filters import ArticleFilter
from api.v1.blog.services import BlogService

from main.pagination import BasePageNumberPagination

logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination


class ArticleViewSet(ViewSet):
    filterset_class = ArticleFilter

    def template_name(self):
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
