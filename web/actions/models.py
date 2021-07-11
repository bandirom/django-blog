from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import LikeDislikeManager
from .choices import LikeStatus

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
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_to')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
