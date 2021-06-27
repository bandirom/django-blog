from typing import Union
from rest_framework import serializers

from blog.services import BlogService
from blog.models import Article, Comment

from .choices import LikeStatus, LikeObjChoice, LikeIconStatus
from .services import ActionsService
from .models import LikeDislike


class LikeDislikeSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    model = serializers.ChoiceField(choices=LikeObjChoice.choices)
    vote = serializers.ChoiceField(choices=LikeStatus.choices)

    def save(self):
        icon_status = LikeIconStatus.LIKED \
            if self.validated_data.get('vote') == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        model = self.validated_data.get('model')
        obj: None = None
        object_id = self.validated_data.get('object_id')
        user = self.context['request'].user
        vote = self.validated_data.get('vote')
        if model == LikeObjChoice.ARTICLE:
            obj: Article = BlogService.get_article(article_id=object_id)
        elif model == LikeObjChoice.COMMENT:
            obj: Comment = BlogService.get_comment(comment_id=object_id)
        if like_dislike := ActionsService.get_like_dislike_obj(object_id, user, obj):
            if like_dislike.vote is not vote:
                like_dislike.vote = vote
                like_dislike.save(update_fields=['vote'])
            else:
                like_dislike.delete()
                icon_status = LikeIconStatus.UNDONE
        else:
            obj.votes.create(user=user, vote=self.validated_data.get('vote'))
        return self._response_data(icon_status, obj)

    def _response_data(self, icon_status: str, obj: Union[Article, Comment]) -> dict:
        data = {
            'status': icon_status,
            'like_count': obj.votes.likes().count(),
            'dislike_count': obj.votes.dislikes().count(),
            'sum_rating': obj.votes.sum_rating(),
        }
        return data


class LikeDislikeRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislike
        fields = ('vote', 'user', 'date')
