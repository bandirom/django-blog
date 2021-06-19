from typing import Union
from rest_framework import serializers

from blog.services import BlogService
from blog.models import Article, Comment

from .choices import LikeStatus, LikeObjChoice
from .services import ActionsService
from .models import LikeDislike


class LikeDislikeSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    model = serializers.ChoiceField(choices=LikeObjChoice.choices)
    vote = serializers.ChoiceField(choices=LikeStatus.choices)

    def save(self):
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
                result = True
            else:
                like_dislike.delete()
                result = False
        else:
            obj.votes.create(user=user, vote=self.validated_data.get('vote'))
            result = True
        return self._response_data(result, obj)

    def _response_data(self, result: bool, obj: Union[Article, Comment]) -> dict:
        data = {
            'result': result,
            'like_count': obj.votes.likes().count(),
            'dislike_count': obj.votes.dislikes().count(),
            'sum_rating': obj.votes.sum_rating(),
        }
        return data


class LikeDislikeRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislike
        fields = ('vote', 'user', 'date')
