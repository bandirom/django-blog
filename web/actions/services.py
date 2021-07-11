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
    def follow_user(user_from, user_to_id: int):
        return Follower.objects.create(user_from=user_from, user_to_id=user_to_id)

    @staticmethod
    def is_user_followed(user, to_user_id: int) -> bool:
        return user.follower_from.filter(user_to_id=to_user_id).exists()

    @staticmethod
    def unfollow_user(user_from, user_to_id: int):
        return user_from.follower_from.filter(user_to_id=user_to_id).delete()
