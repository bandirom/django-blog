from django.conf import settings
from django.db.models import Count, QuerySet

from .choices import ArticleStatus
from .models import Category, Article, Comment


class BlogService:

    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    @staticmethod
    def get_active_articles() -> QuerySet[Article]:
        return Article.objects.filter(status=ArticleStatus.ACTIVE).annotate(comments_count=Count('comment_set'))

    @staticmethod
    def get_comments_queryset() -> QuerySet[Comment]:
        return Comment.objects.select_related('article').filter(article__status=ArticleStatus.ACTIVE)

    @staticmethod
    def is_valid_comment_parent(parent_id: int, article: Article):
        return Comment.objects.filter(id=parent_id, article=article, parent__isnull=True).exists()
