from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from . import serializers
from .filters import ArticleFilter
from .services import BlogService, CommentQueryService


class ArticleListView(ListAPIView):
    filterset_class = ArticleFilter
    serializer_class = serializers.ArticleSerializer
    permission_classes = ()

    def get_queryset(self):
        return BlogService().get_active_articles()


class ArticleDetailView(GenericAPIView):
    permission_classes = ()
    serializer_class = serializers.FullArticleSerializer

    def get_object(self):
        return BlogService().get_article_by_slug(self.kwargs['slug'])

    def get(self, request, slug: str):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class CreateArticleView(GenericAPIView):
    serializer_class = serializers.CreateArticleSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentListView(ListAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        slug = self.kwargs['article_slug']
        return CommentQueryService().comments_by_article_slug(slug)
