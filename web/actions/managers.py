from django.db import models
from django.db.models import Sum
from .choices import LikeStatus, LikeObjChoice


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote=LikeStatus.LIKE)

    def dislikes(self):
        return self.get_queryset().filter(vote=LikeStatus.DISLIKE)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model=LikeObjChoice.ARTICLE).order_by('-articles__updated')

    def comments(self):
        return self.get_queryset().filter(content_type__model=LikeObjChoice.COMMENT).order_by('-comments__updated')

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'content_type').prefetch_related('content_object')
