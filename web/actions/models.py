from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import LikeDislikeManager
from .choices import LikeStatus, UserActionsChoice

User = get_user_model()


class LikeDislike(models.Model):
    vote = models.SmallIntegerField(choices=LikeStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateTimeField(auto_now_add=True)

    objects = LikeDislikeManager()

    def __str__(self):
        return "{user}: {vote} - {content}".format(user=self.user, vote=self.vote, content=self.content_object)


class Follower(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-created',)
        unique_together = ('subscriber', 'to_user')

    def __str__(self):
        return f'{self.subscriber} follows {self.to_user}'


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    action = models.PositiveSmallIntegerField(choices=UserActionsChoice.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey()
    date = models.DateTimeField(auto_now_add=True, db_index=True)
