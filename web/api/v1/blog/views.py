from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from . import serializers
from .filters import ArticleFilter
from .services import BlogService


class ArticleListView(ListAPIView):
    filterset_class = ArticleFilter
    serializer_class = serializers.ArticleSerializer
    permission_classes = ()

    def get_queryset(self):
        return BlogService.get_active_articles()


class ArticleDetailView(GenericAPIView):
    permission_classes = ()
    serializer_class = serializers.FullArticleSerializer

    def get(self, request):

        return Response()
