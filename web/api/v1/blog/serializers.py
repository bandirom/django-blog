from rest_framework import serializers

from actions.choices import LikeIconStatus, LikeStatus
from actions.serializers import LikeDislikeRelationSerializer
from api.v1.blog.services import BlogService
from blog.models import Article
from blog.serializers import CategorySerializer, CommentSerializer
from main.taggit_serializers import TagListSerializerField, TaggitSerializer
from user_profile.serializers import ShortUserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = ShortUserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    like_status = serializers.SerializerMethodField(method_name='get_like_status')

    def get_like_status(self, obj) -> str:
        user = self.context['request'].user
        if not user.is_authenticated:
            return LikeIconStatus.UNDONE
        if like_obj := obj.votes.filter(user=user).first():
            return LikeIconStatus.LIKED if like_obj.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        return LikeIconStatus.UNDONE

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
    # comments = serializers.SerializerMethodField('get_parent_comment')
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

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_title(self, title: str):
        if BlogService.is_article_slug_exist(title):
            raise serializers.ValidationError("This title already exists")
        return title