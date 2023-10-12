from typing import Optional, Self, TypeVar
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.reverse import reverse

from blog.choices import ArticleStatus

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')


def avatar_upload_path(obj: 'User', filename: str) -> str:
    return f"avatars/{obj.id}/{filename}"


class GenderChoice(models.IntegerChoices):
    MALE = 0, _('Male')
    Female = 1, _('Female')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    avatar = models.ImageField(default='no-avatar.png', blank=True, upload_to=avatar_upload_path)
    birthday = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GenderChoice.choices, null=True, blank=True)
    website = models.URLField(blank=True, default='')

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []
    following = models.ManyToManyField('self', through='actions.Follower', symmetrical=False, related_name='followers')

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)

    @classmethod
    def from_key(cls, key: str) -> Optional[Self]:
        max_age = 60 * 60 * 24 * settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        try:
            pk = signing.loads(key, max_age=max_age)
            user = cls.objects.get(id=pk)
        except (signing.SignatureExpired, signing.BadSignature, cls.DoesNotExist):
            user = None
        return user

    def user_likes(self) -> int:
        return self.likes.all().count()

    def user_posts(self) -> int:
        return self.article_set.filter(status=ArticleStatus.ACTIVE).count()

    def followers_count(self) -> int:
        return self.followers.count()

    def following_count(self) -> int:
        return self.following.count()

    def get_absolute_url(self) -> str:
        return reverse('user_profile:user_by_id', args=(self.id,))

    @cached_property
    def avatar_url(self) -> str:
        return urljoin(settings.BACKEND_URL, self.profile.avatar.url)

    @cached_property
    def full_profile_url(self) -> str:
        return urljoin(settings.BACKEND_URL, self.get_absolute_url())

    def set_image_to_default(self):
        self.avatar.delete(save=False)  # delete old image file

    def is_default_image(self):
        return True if self.avatar.url.find("no-avatar.png") != -1 else False
