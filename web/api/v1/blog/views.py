from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .filters import ArticleFilter
from .services import BlogQueryService, CommentQueryService, TagQueryService


class ArticleListView(ListAPIView):
    filterset_class = ArticleFilter
    serializer_class = serializers.ArticleSerializer
    permission_classes = ()

    def get_queryset(self):
        return BlogQueryService().get_articles(self.request.user)


class ArticleDetailView(GenericAPIView):
    permission_classes = ()
    serializer_class = serializers.FullArticleSerializer

    def get_object(self):
        return BlogQueryService().get_article_by_slug(self.kwargs['slug'], self.request.user)

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
    serializer_class = serializers.CommentListSerializer

    def get_queryset(self):
        slug = self.kwargs['article_slug']
        return CommentQueryService().comments_by_article_slug(slug, self.request.user)


class CreateCommentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CreateCommentSerializer


class TagListView(ListAPIView):
    serializer_class = serializers.TagListSerializer
    pagination_class = None

    def get_queryset(self):
        return TagQueryService().popular_tags()
