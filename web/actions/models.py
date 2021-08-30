from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import LikeDislikeManager, FollowerManager
from .choices import LikeStatus

User = get_user_model()


def like_content_limit():
    return (
        models.Q(app_label='blog', model='article') |
        models.Q(app_label='blog', model='comment')
    )


class LikeDislike(models.Model):
    vote = models.SmallIntegerField(choices=LikeStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=like_content_limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField(auto_now=True)

    objects = LikeDislikeManager()

    def __str__(self):
        return "{user}: {vote} - {content}".format(user=self.user, vote=self.vote, content=self.content_object)


class Follower(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_to')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = FollowerManager()

    class Meta:
        ordering = ('-created',)
        unique_together = ('subscriber', 'to_user')

    def __str__(self):
        return f'{self.subscriber} follow to {self.to_user}'


def action_content_limit():
    return (
        models.Q(app_label='actions', model='follower') |
        models.Q(app_label='actions', model='likedislike') |
        models.Q(app_label='user_profile', model='profile')
    )


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=500)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=action_content_limit)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey()
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-date',)
