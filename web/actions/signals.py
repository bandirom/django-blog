from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .services import ActionsService
from .models import Follower, LikeDislike
from .choices import LikeObjChoice, LikeStatus
from user_profile.models import Profile


@receiver(post_save, sender=Follower)
def user_start_to_follow(sender, created: bool, instance: Follower, **kwargs):
    template = 'actions/action_templates/start_to_follow.html'
    data = {
        'subscriber': instance.subscriber,
        'to_user': instance.to_user
    }
    action = render_to_string(template, data)
    ActionsService.create_action(instance.subscriber, action, instance)


@receiver(post_save, sender=Profile)
def user_change_avatar(sender, created: bool, instance: Profile, update_fields: frozenset, **kwargs):
    if created or not update_fields:
        return
    if 'avatar' not in update_fields:
        return
    template = 'actions/action_templates/change_avatar.html'
    data = {
        'avatar_url': instance.avatar,
        'user': instance.user
    }
    action = render_to_string(template, data)
    ActionsService.create_action(instance.user, action, instance)


@receiver(post_save, sender=LikeDislike)
def user_like_article(sender, created: bool, instance: LikeDislike, **kwargs):
    if instance.content_type.model != LikeObjChoice.ARTICLE:
        return
    template = 'actions/action_templates/user_like_article.html'
    data = {
        'user': instance.user,
        'article': instance.content_object,
        'vote': 'like' if instance.vote == LikeStatus.LIKE else 'dislike',
    }
    action = render_to_string(template, data)
    ActionsService.create_action(instance.user, action, instance)
