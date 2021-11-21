from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from main.decorators import except_shell
from .models import LikeDislike, Follower, Action
from blog.models import Article, Comment

User = get_user_model()


class ActionsService:

    @staticmethod
    @except_shell(User.DoesNotExist)
    def get_user_by_id(user_id: int):
        return User.objects.get(id=user_id)

    @staticmethod
    def get_content_object(model_object):
        return ContentType.objects.get_for_model(model_object)

    @staticmethod
    @except_shell((LikeDislike.DoesNotExist,))
    def get_like_dislike_obj(object_id: int, user, model_object: Union[Article, Comment]) -> LikeDislike:
        content_type = ActionsService.get_content_object(model_object)
        return LikeDislike.objects.get(content_type=content_type, object_id=object_id, user=user)

    @staticmethod
    def follow_user(user, to_user_id: int):
        return Follower.objects.create(subscriber=user, to_user_id=to_user_id)

    @staticmethod
    def is_user_followed(user, to_user_id: int) -> bool:
        return Follower.objects.filter(subscriber=user, to_user_id=to_user_id).exists()

    @staticmethod
    def unfollow_user(user, to_user_id: int):
        return Follower.objects.filter(subscriber=user, to_user_id=to_user_id).delete()

    @staticmethod
    def create_action(user, action: str, target):
        return Action.objects.create(user=user, action=action, content_object=target)

    @staticmethod
    def get_user_followers(user):
        return user.followers.select_related('profile').all()

    @staticmethod
    def get_user_following(user):
        return user.following.select_related('profile').all()

    @staticmethod
    def get_following_actions(user):
        followings = user.following.all()
        return Action.objects.filter(user__in=followings)
