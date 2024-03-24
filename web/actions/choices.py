from enum import Enum

from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class LikeStatus(IntegerChoices):
    LIKE = (1, _('Like'))
    DISLIKE = (-1, _('Dislike'))


class LikeObjChoice(TextChoices):
    ARTICLE = ('article', _('Article'))
    COMMENT = ('comment', _('Comment'))


class LikeIconStatus(IntegerChoices):
    LIKED = 1
    DISLIKED = -1
    EMPTY = 0


class FollowStatus(Enum):
    FOLLOW = True
    UNFOLLOW = False


class UserActionsChoice(IntegerChoices):
    FOLLOW_TO = (1, _('User {subscriber} follow to {user_to}'))
    UNFOLLOW_TO = (2, _('User {subscriber} unfollow user {user_to}'))
    LIKED_ARTICLE = (3, _('User {user} liked article {article}'))
    DISLIKED_ARTICLE = (4, _('User {user} disliked article {article}'))
    LIKED_COMMENT = (5, _('User {user} liked comment {comment} from user {comment_owner}'))


class ActionFeed(TextChoices):
    UPDATE_AVATAR = 'update_avatar'
    CREATE_ARTICLE = 'create_article'
