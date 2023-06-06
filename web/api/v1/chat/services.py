
from typing import TYPE_CHECKING
from django.contrib.auth import get_user_model
from .serializers import UserShortInfoSerializer


User = get_user_model()


if TYPE_CHECKING:
    from django.db.models import QuerySet


class UserDataHandler:

    def user_queryset(self, user_ids: list[int]) -> "QuerySet[User]":
        return User.objects.select_related('profile').filter(id__in=user_ids)

    def get_user_data(self, user_ids: list[int]) -> dict:
        users = self.user_queryset(user_ids)
        user_data: list[dict] = UserShortInfoSerializer(users, many=True).data
        users_data: dict[int, dict] = {}
        for user in user_data:
            users_data[user['id']] = user
        return users_data
