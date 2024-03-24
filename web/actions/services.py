from django.contrib.auth import get_user_model

from .models import Action
from main.decorators import except_shell

User = get_user_model()


class ActionsService:
    @staticmethod
    @except_shell(User.DoesNotExist)
    def get_user_by_id(user_id: int):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_action(user, action: str, target):
        return Action.objects.create(user=user, action=action, content_object=target)

    @staticmethod
    def get_following_actions(user):
        followings = user.following.all()
        return Action.objects.filter(user__in=followings)
