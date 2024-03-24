from django.db import models


class SocialAccountProvider(models.TextChoices):
    GOOGLE = 'google'
    FACEBOOK = 'facebook'


class SocialAccount(models.Model):
    user = models.ForeignKey('main.User', on_delete=models.CASCADE, related_name='social_accounts')
    uid = models.CharField(max_length=40, blank=True, null=True, unique=True)
    provider = models.CharField(max_length=20, choices=SocialAccountProvider.choices)
    connected = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'provider'), name='unique_user_provider'),
            models.UniqueConstraint(fields=('provider', 'uid'), name='unique_uid_provider'),
        ]
        indexes = [
            models.Index(fields=('provider', 'uid')),
        ]
