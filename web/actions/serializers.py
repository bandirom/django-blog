from typing import Union
from rest_framework import serializers

from blog.services import BlogService
from blog.models import Article, Comment

from .choices import LikeStatus, LikeObjChoice, LikeIconStatus, FollowIconStatus
from .services import ActionsService
from .models import LikeDislike


class LikeDislikeSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(min_value=1)
    model = serializers.ChoiceField(choices=LikeObjChoice.choices)
    vote = serializers.ChoiceField(choices=LikeStatus.choices)

    def save(self):
        vote = self.validated_data.get('vote')

        icon_status = LikeIconStatus.LIKED if vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED
        model = self.validated_data.get('model')
        object_id = self.validated_data.get('object_id')
        user = self.context['request'].user
        if model == LikeObjChoice.ARTICLE:
            obj: Article = BlogService.get_article(article_id=object_id)
        else:
            obj: Comment = BlogService.get_comment(comment_id=object_id)
        if like_dislike := ActionsService.get_like_dislike_obj(object_id, user, obj):
            if like_dislike.vote is not vote:
                like_dislike.vote = vote
                like_dislike.save(update_fields=['vote'])
            else:
                like_dislike.delete()
                icon_status = LikeIconStatus.UNDONE
        else:
            obj.votes.create(user=user, vote=vote)
        return self._response_data(icon_status, obj)

    def _response_data(self, icon_status: str, obj: Union[Article, Comment]) -> dict:
        data = {
            'status': icon_status,
            'like_count': obj.likes(),
            'dislike_count': obj.dislikes(),
            'sum_rating': obj.votes.sum_rating(),
        }
        return data


class LikeDislikeRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislike
        fields = ('vote', 'user', 'date')


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)

    def save(self) -> dict:
        user = self.context['request'].user
        user_id = self.validated_data.get('user_id')
        if not ActionsService.is_user_followed(user, user_id):
            ActionsService.follow_user(user, user_id)
            follow_status = FollowIconStatus.UNFOLLOW
        else:
            ActionsService.unfollow_user(user, user_id)
            follow_status = FollowIconStatus.FOLLOW
        return self.response_data(follow_status)

    def response_data(self, follow_status: str) -> dict:
        return {
            'status': follow_status,
        }
