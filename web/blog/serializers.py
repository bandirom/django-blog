from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Article, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'updated')


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count')


class FullArticleSerializer(ArticleSerializer):

    comments = CommentSerializer(source='comment_set', many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('content', 'comments',)
