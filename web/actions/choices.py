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
