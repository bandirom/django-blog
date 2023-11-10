from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from actions.choices import LikeIconStatus, LikeStatus
from api.v1.blog.serializers import CategorySerializer
from api.v1.blog.services import BlogService
from user_profile.serializers import ShortUserSerializer

from .models import Article, Comment
from main.taggit_serializers import TaggitSerializer, TagListSerializerField

User = get_user_model()


class ParentCommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    def get_like_status(self, obj) -> str:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.UNDONE
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.UNDONE

    class Meta:
        model = Comment
        fields = ('id', 'content', 'updated', 'article', 'user', 'like_status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    child = ParentCommentSerializer(many=True, read_only=True, source='parent_set')
    parent_id = serializers.IntegerField(min_value=1, default=None)
    user = ShortUserSerializer(read_only=True)
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    def get_like_status(self, obj) -> str:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.UNDONE
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.UNDONE

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

    def validate(self, data):
        if not self.context.get('request').user.is_authenticated and not data.get('author'):
            raise serializers.ValidationError({'author': _('Please enter your email or log in')})
        parent_id = data.get('parent_id')
        if parent_id and not BlogService.is_valid_comment_parent(parent_id, data.get('article')):
            raise serializers.ValidationError({'parent_id': _('Choice comment is not valid for this article')})
        return data

    def create(self, validated_data: dict):
        user = self.context.get('request').user
        if user.is_authenticated:
            validated_data['user'] = user
        return Comment.objects.create(**validated_data)


class UpdateDestroyCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()

    class Meta:
        model = Comment

        fields = (
            'id',
            'content',
            'updated',
        )

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.is_authenticated and user != self.instance.user:
            if self.context.get('request').method == 'PUT':
                raise serializers.ValidationError({'content': _('You can not edit this comment')})
            raise serializers.ValidationError({'content': _('You can not delete this comment')})
        return attrs


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = ShortUserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

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
            'tag_list',
        )


class FullArticleSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields


class CreateArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ('title', 'category', 'image', 'content', 'tags')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_title(self, title: str):
        if BlogService.is_article_slug_exist(title):
            raise serializers.ValidationError("This title already exists")
        return title
