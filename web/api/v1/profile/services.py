from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, Q

from actions.models import Follower
from blog.choices import ArticleStatus

from main.decorators import except_shell

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from main.models import UserType


User: 'UserType' = get_user_model()


class UserQueryService:
    @staticmethod
    def get_queryset(is_active: Optional[bool] = None) -> 'QuerySet[User]':
        """Return user queryset
        If is_active is None -> return all users
        Otherwise filter by is_active field
        """
        queryset = User.objects.all()
        if is_active is None:
            return queryset
        return queryset.filter(is_active=is_active)

    def user_profile_queryset(self) -> 'QuerySet[User]':
        user_articles = Count('article_set', filter=Q(article_set__status=ArticleStatus.ACTIVE))
        user_likes = Count('likes')
        return self.get_queryset(is_active=True).annotate(user_posts=user_articles, user_likes=user_likes)

    @staticmethod
    def exist_annotation(user) -> Exists:
        return Exists(Follower.objects.filter(subscriber=user, to_user_id=OuterRef('pk')))

    def user_list_queryset(self, current_user: User) -> 'QuerySet[User]':
        return self.user_profile_queryset().annotate(follow=self.exist_annotation(current_user))

    @except_shell((User.DoesNotExist,), raise_404=True)
    def get_user_by_id(self, user_id: int, extend: bool = False) -> User:
        if extend:
            return self.user_profile_queryset().get(id=user_id)
        return self.get_queryset().get(id=user_id)

    def get_user_followers(self, user: User) -> 'QuerySet[User]':
        return user.followers.all().annotate(follow=self.exist_annotation(user))

    def get_user_following(self, user: User) -> 'QuerySet[User]':
        return user.following.all().annotate(follow=self.exist_annotation(user))
