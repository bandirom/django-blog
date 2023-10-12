from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, QuerySet

from blog.choices import ArticleStatus

User = get_user_model()


class UserProfileService:
    @staticmethod
    def get_user_profile(user_id: int) -> User:
        user_articles = Count('article_set', filter=Q(article_set__status=ArticleStatus.ACTIVE))
        user_likes = Count('likes')
        return User.objects.annotate(user_posts=user_articles, user_likes=user_likes).get(id=user_id)

    @staticmethod
    def user_queryset() -> QuerySet[User]:
        return User.objects.exclude(is_active=False)

    @staticmethod
    def get_users_by_list_id(user_ids: list) -> QuerySet[User]:
        queryset = UserProfileService.user_queryset()
        return queryset.filter(id__in=user_ids)
