from django.db import transaction
from rest_framework import serializers

from actions.choices import LikeIconStatus, LikeStatus
from actions.serializers import LikeDislikeRelationSerializer
from api.v1.blog.services import BlogService, CommentQueryService
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
    like_status = serializers.SerializerMethodField(method_name='get_like_status')
    tags = TagListSerializer(many=True)

    def get_like_status(self, obj: Article) -> LikeIconStatus:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.EMPTY
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.EMPTY

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
            'like_status',
            'tags',
        )


class FullArticleSerializer(ArticleSerializer):
    votes = LikeDislikeRelationSerializer(many=True)

    def get_parent_comment(self, obj):
        queryset = obj.comment_set.filter(parent_id__isnull=True)
        return CommentSerializer(queryset, source='comment_set', many=True).data

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('votes',)


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ('title', 'category', 'image', 'content', 'tags')

    @transaction.atomic()
    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_title(self, title: str):
        if BlogService.is_article_slug_exist(title):
            raise serializers.ValidationError("This title already exists")
        return title


class ParentCommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    def get_like_status(self, obj) -> LikeIconStatus:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.EMPTY
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.EMPTY

    class Meta:
        model = Comment
        fields = ('id', 'content', 'updated', 'article', 'user', 'like_status')


class CommentSerializer(serializers.ModelSerializer):
    child = ParentCommentSerializer(many=True, read_only=True, source='parent_set')
    parent_id = serializers.IntegerField(min_value=1, default=None)
    user = ShortUserSerializer(read_only=True)
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    def get_like_status(self, obj) -> LikeIconStatus:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.EMPTY
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.EMPTY

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'child',
            'updated',
            'article',
            'parent_id',
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
