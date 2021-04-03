import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .services import BlogService
from . import serializers
from main.pagination import DefaultPagination

logger = logging.getLogger(__name__)


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = DefaultPagination

    def get_queryset(self):
        return BlogService.category_queryset()
