from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from actions.choices import FollowIconStatus, LikeIconStatus, LikeObjChoice, LikeStatus
from actions.models import Follower, LikeDislike
from blog.models import Article, Comment

from main.models import UserType

User: UserType = get_user_model()


class LikeService:
    def __init__(self, user: User, vote: LikeStatus, model: LikeObjChoice, object_id: int):
        self.user = user
        self.vote = vote
        self.model = model
        self.object_id = object_id
        self.instance = self.model_instance()

    def get_content_type_for_model(self) -> ContentType:
        return ContentType.objects.get_for_model(self.model_instance())

    def get_article(self) -> Article:
        return Article.objects.get(id=self.object_id)

    def get_comment(self) -> Comment:
        return Comment.objects.get(id=self.object_id)

    def model_instance(self) -> Article | Comment:
        obj = None
        match self.model:
            case LikeObjChoice.ARTICLE:
                obj = self.get_article()
            case LikeObjChoice.COMMENT:
                obj = self.get_comment()
        return obj

    def get_like_object(self) -> Optional[LikeDislike]:
        content_type = self.get_content_type_for_model()
        return LikeDislike.objects.filter(
            content_type=content_type, object_id=self.object_id, user=self.user
        ).first()

    def create_like_object(self) -> LikeDislike:
        return self.instance.votes.create(user=self.user, vote=self.vote)

    def update_like_object(self, obj: LikeDislike) -> LikeDislike:
        obj.vote = self.vote
        obj.save(update_fields=['vote'])
        return obj

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

        data = {
            'status': _status,
            'like_count': self.instance.likes(),
            'dislike_count': self.instance.dislikes(),
        }
        return data


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

    def subscribe(self) -> dict:
        if not self.is_user_subscribed():
            self.subscribe_to_user()
            follow_status = FollowIconStatus.UNFOLLOW
        else:
            self.unfollow_user()
            follow_status = FollowIconStatus.FOLLOW
        return {
            'status': follow_status,
        }
