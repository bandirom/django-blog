from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import Case, Count, IntegerField, Q, QuerySet, Value, When
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

from actions.choices import ActionFeed, FollowStatus, LikeIconStatus, LikeObjChoice, LikeStatus
from actions.models import Action, Follower, LikeDislike
from blog.models import Article, Comment

from main.decorators import except_shell
from main.models import UserType

User: UserType = get_user_model()


class LikeQueryService:
    @staticmethod
    def like_annotate(user):
        if not user.is_authenticated:
            return Value(LikeIconStatus.EMPTY, output_field=IntegerField())
        return Case(
            When(votes__user=user, votes__vote=LikeStatus.LIKE, then=Value(LikeIconStatus.LIKED)),
            When(votes__user=user, votes__vote=LikeStatus.DISLIKE, then=Value(LikeIconStatus.DISLIKED)),
            default=Value(LikeIconStatus.EMPTY),
            output_field=IntegerField(),
        )


class LikeService:
    def __init__(self, user: User, vote: LikeStatus, model: LikeObjChoice, object_id: int):
        self.user = user
        self.vote = vote
        self.model = model
        self.object_id = object_id
        self.instance = self.model_instance()

    @except_shell((Article.DoesNotExist,), raise_404=True)
    def get_article(self) -> Article:
        return Article.objects.get(id=self.object_id)

    @except_shell((Comment.DoesNotExist,), raise_404=True)
    def get_comment(self) -> Comment:
        return Comment.objects.get(id=self.object_id)

    def model_instance(self) -> Article | Comment:
        match self.model:
            case LikeObjChoice.ARTICLE:
                return self.get_article()
            case LikeObjChoice.COMMENT:
                return self.get_comment()

    def get_like_object(self) -> Optional[LikeDislike]:
        return self.instance.votes.filter(user=self.user).first()

    def create_like_object(self) -> LikeDislike:
        return self.instance.votes.create(user=self.user, vote=self.vote)

    def update_like_object(self, obj: LikeDislike) -> LikeDislike:
        obj.vote = self.vote
        obj.save(update_fields=['vote'])
        return obj

    def _get_vote_count(self) -> dict:
        return self.instance.votes.aggregate(
            like_count=Count('vote', filter=Q(vote=LikeStatus.LIKE)),
            dislike_count=Count('vote', filter=Q(vote=LikeStatus.DISLIKE)),
        )

    def make_like(self) -> dict:
        _status = LikeIconStatus.LIKED if self.vote == LikeStatus.LIKE else LikeIconStatus.DISLIKED

        if like_obj := self.get_like_object():
            if like_obj.vote is not self.vote:
                self.update_like_object(like_obj)
            else:
                like_obj.delete()
                _status = LikeIconStatus.EMPTY
        else:
            self.create_like_object()

        aggregated_result = self._get_vote_count()
        aggregated_result['status'] = _status
        return aggregated_result


class FollowService:
    def __init__(self, user: User, user_id: int):
        self.user = user
        self.to_user_id = user_id

    def is_user_subscribed(self) -> bool:
        return Follower.objects.filter(subscriber=self.user, to_user_id=self.to_user_id).exists()

    def subscribe_to_user(self) -> Follower:
        return Follower.objects.create(subscriber=self.user, to_user_id=self.to_user_id)

    def unfollow_user(self):
        return Follower.objects.filter(subscriber=self.user, to_user_id=self.to_user_id).delete()

    def subscribe(self) -> bool:
        if not self.is_user_subscribed():
            self.subscribe_to_user()
            follow_status = FollowStatus.FOLLOW
        else:
            self.unfollow_user()
            follow_status = FollowStatus.UNFOLLOW
        return follow_status.value


class ActivityService:
    def __init__(self, action: ActionFeed, user: User, content_object):
        self.action = action
        self.user = user
        self.content_object = content_object

    def create_activity(self) -> Action:
        return Action.objects.create(user=self.user, action=self.action, content_object=self.content_object)
