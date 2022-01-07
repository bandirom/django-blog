from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.reverse import reverse_lazy

from blog.choices import ArticleStatus
from .managers import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(_('Email address'), unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    following = models.ManyToManyField('self', through='actions.Follower', symmetrical=False, related_name='followers')
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def full_name(self) -> str:
        return super().get_full_name()

    def email_verified(self) -> bool:
        return self.emailaddress_set.get(primary=True).verified
    email_verified.boolean = True

    def user_likes(self) -> int:
        return self.likes.all().count()

    def user_posts(self) -> int:
        return self.article_set.filter(status=ArticleStatus.ACTIVE).count()

    def followers_count(self) -> int:
        return self.followers.count()

    def following_count(self) -> int:
        return self.following.count()

    def get_absolute_url(self):
        return reverse_lazy('user_profile:user_by_id', args=(self.id,))

    @cached_property
    def avatar_url(self) -> str:
        return urljoin(settings.BACKEND_SITE, self.profile.avatar.url)

    @cached_property
    def full_profile_url(self):
        return urljoin(settings.BACKEND_SITE, str(self.get_absolute_url()))
