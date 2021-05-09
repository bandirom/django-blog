from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .choices import GenderChoice

User = get_user_model()


def avatar_upload_patch(obj, filename: str):
    return f"avatars/{obj.user_id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='no-avatar.png', blank=True, upload_to=avatar_upload_patch)
    birthday = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GenderChoice.choices, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Profile')
