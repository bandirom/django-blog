import logging

from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.v1.blog.serializers import CategorySerializer
from api.v1.blog.services import BlogService

from . import serializers
from main.pagination import BasePageNumberPagination
from main.views import TemplateAPIView

logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination


class CreateArticleTemplateView(TemplateAPIView):
    template_name = 'blog/post_create.html'

    def get_queryset(self):
        return BlogService.category_queryset()

    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        data = {'categories': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
