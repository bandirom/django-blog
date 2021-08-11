from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.reverse import reverse_lazy

from .services import ActionsService
from .models import Follower
from .choices import UserActionsChoice


@receiver(post_save, sender=Follower)
def user_start_to_follow(sender, created: bool, instance: Follower, **kwargs):
    subscriber = user_profile_html_link(instance.subscriber)
    user_to = user_profile_html_link(instance.to_user)
    action = UserActionsChoice.FOLLOW_TO.label.format(subscriber=subscriber, user_to=user_to)
    ActionsService.create_action(instance.subscriber, action, instance)


def user_profile_html_link(user) -> str:
    url = reverse_lazy("user_profile:user_by_id", args=(user.id,))
    return '<a href="{url}">{full_name}</a>'.format(url=url, full_name=user.full_name())
