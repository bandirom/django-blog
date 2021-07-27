from typing import Union

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from main.decorators import except_shell
from .models import LikeDislike, Follower
from blog.models import Article, Comment


class ActionsService:

    @staticmethod
    @except_shell((LikeDislike.DoesNotExist,))
    def get_like_dislike_obj(object_id: int, user, model_object: Union[Article, Comment]) -> LikeDislike:
        content_type = ContentType.objects.get_for_model(model_object)
        return LikeDislike.objects.get(content_type=content_type, object_id=object_id, user=user)

    @staticmethod
    def follow_user(user, to_user_id: int):
        return Follower.objects.create(subscriber=user, to_user_id=to_user_id)

    @staticmethod
    def is_user_followed(user, to_user_id: int) -> bool:
        return user.following.filter(to_user_id=to_user_id).exists()

    @staticmethod
    def unfollow_user(user, to_user_id: int):
        return user.following.filter(to_user_id=to_user_id).delete()
