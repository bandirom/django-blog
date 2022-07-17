from django.db import models

from .choices import ArticleStatus


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ArticleStatus.ACTIVE)
