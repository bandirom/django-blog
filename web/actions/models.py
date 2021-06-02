from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import LikeDislikeManager
from .choices import LikeStatus


User = get_user_model()


class LikeDislike(models.Model):
    vote = models.SmallIntegerField(choices=LikeStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __str__(self):
        return "{user}: {vote} - {content}".format(user=self.user, vote=self.vote, content=self.content_object)
