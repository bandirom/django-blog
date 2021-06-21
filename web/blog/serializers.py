from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from actions.serializers import LikeDislikeRelationSerializer
from user_profile.serializers import UserSerializer
from .models import Category, Article, Comment
from .services import BlogService


class ParentCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'updated', 'article', 'user')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.EmailField(required=False)
    child = ParentCommentSerializer(many=True, read_only=True, source='parent_set')
    parent_id = serializers.IntegerField(min_value=1, default=None)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'child', 'updated', 'article', 'parent_id')

    def validate(self, data):
        if not self.context.get('request').user.is_authenticated and not data.get('author'):
            raise serializers.ValidationError({'author': _('Please enter your email or log in')})
        parent_id = data.get('parent_id')
        if parent_id and not BlogService.is_valid_comment_parent(parent_id, data.get('article')):
            raise serializers.ValidationError({'parent_id': _('Choice comment is not valid for this article')})
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.is_authenticated:
            validated_data['author'] = user.email
            validated_data['user'] = user
        return Comment.objects.create(**validated_data)


class UpdateDestroyCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()

    class Meta:
        model = Comment

        fields = ('id', 'content', 'updated',)

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated and user != self.instance.user:
            if self.context.get('request').method == 'PUT':
                raise serializers.ValidationError({'content': _('You can not edit this comment')})
            raise serializers.ValidationError({'content': _('You can not delete this comment')})
        return attrs


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
        fields = (
            'id', 'title', 'url', 'author', 'category', 'likes', 'dislikes',
            'created', 'updated', 'comments_count', 'image', 'content'
        )


class FullArticleSerializer(ArticleSerializer):
    comments = CommentSerializer(source='comment_set', many=True)
    votes = LikeDislikeRelationSerializer(many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('comments', 'votes')


class CreateArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('title', 'category', 'image', 'content')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_title(self, title: str):
        if BlogService.is_article_slug_exist(title):
            raise serializers.ValidationError("This title already exists")
        return title
