from typing import Union

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from main.decorators import except_shell
from .models import LikeDislike
from blog.models import Article, Comment


class ActionsService:

    @staticmethod
    @except_shell((LikeDislike.DoesNotExist,))
    def get_like_dislike_obj(object_id: int, user, model_object: Union[Article, Comment]) -> LikeDislike:
        content_type = ContentType.objects.get_for_model(model_object)
        return LikeDislike.objects.get(content_type=content_type, object_id=object_id, user=user)
