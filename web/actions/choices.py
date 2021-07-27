from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class LikeStatus(IntegerChoices):
    LIKE = (1, _('Like'))
    DISLIKE = (-1, _('Dislike'))


class LikeObjChoice(TextChoices):
    ARTICLE = ('article', _('Article'))
    COMMENT = ('comment', _('Comment'))


class LikeIconStatus(TextChoices):
    LIKED = ('liked', _('Liked'))
    DISLIKED = ('disliked', _('Disliked'))
    UNDONE = ('undone', _('Undone'))


class FollowIconStatus(TextChoices):
    FOLLOW = ('Follow', _('Follow'))
    UNFOLLOW = ('Unfollow', _('Unfollow'))


class UserActionsChoice(IntegerChoices):
    FOLLOW_TO = (1, _('User {subscriber} follow to {user_to}'))
    LIKED_ARTICLE = (2, _('User {user} liked article {article}'))
    DISLIKED_ARTICLE = (3, _('User {user} disliked article {article}'))
    LIKED_COMMENT = (4, _('User {user} liked comment {comment} from user {comment_owner}'))
