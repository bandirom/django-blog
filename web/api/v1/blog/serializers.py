from django.db import transaction
from rest_framework import serializers

from actions.choices import LikeIconStatus, LikeStatus
from actions.serializers import LikeDislikeRelationSerializer
from api.v1.blog.services import CommentQueryService
from blog.models import Article, ArticleTag, Category, Comment
from user_profile.serializers import ShortUserSerializer

from main.taggit_serializers import TaggitSerializer, TagListSerializerField


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ('id', 'slug', 'name')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = ShortUserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    like_status = serializers.IntegerField()
    tags = TagListSerializer(many=True)
    truncated_text = serializers.CharField()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'url',
            'author',
            'category',
            'likes',
            'dislikes',
            'created',
            'updated',
            'comments_count',
            'image',
            'content',
            'truncated_text',
            'like_status',
            'tags',
        )


class FullArticleSerializer(ArticleSerializer):
    votes = LikeDislikeRelationSerializer(many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('votes',)


class CreateArticleSerializer(serializers.ModelSerializer):  # TaggitSerializer,
    tags = serializers.CharField()

    def validate_tags(self, tags: str) -> list[str]:
        return tags.split(',')

    class Meta:
        model = Article
        fields = (
            'title',
            'category',
            'image',
            'content',
            'tags',
        )


class ParentCommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'updated',
            'user',
        )


class CommentListSerializer(serializers.ModelSerializer):
    children = ParentCommentSerializer(many=True, read_only=True, source='parent_set')
    user = ShortUserSerializer(read_only=True)
    like_status = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'children',
            'updated',
            'like_status',
        )


class CreateCommentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'parent_id',
            'article',
            'content',
        )

    def validate(self, data: dict):
        parent_id = data.get('parent_id')
        if parent_id and not CommentQueryService.is_valid_comment_parent(parent_id, data['article']):
            raise serializers.ValidationError({'parent_id': 'Selected comment is not valid for this article'})
        return data

    def create(self, validated_data: dict):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
