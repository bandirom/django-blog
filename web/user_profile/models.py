from django.contrib.auth import get_user_model
from django.db import models
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
    website = models.URLField(blank=True, default='')

    objects = models.Manager()

    class Meta:
        verbose_name = _('Profile')

    def set_image_to_default(self):
        self.avatar.delete(save=False)  # delete old image file
        self.save()

    def is_default_image(self):
        return True if self.avatar.url.find("no-avatar.png") != -1 else False

    def __str__(self):
        return f"{self.user.full_name()} profile"
