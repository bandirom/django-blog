from django.db.models import Count

from blog.choices import ArticleStatus
from blog.models import Article, Category


class BlogService:
    @staticmethod
    def category_queryset():
        return Category.objects.all()

    @staticmethod
    def get_active_articles():
        return Article.objects.filter(status=ArticleStatus.ACTIVE).annotate(comments_count=Count('comment_set'))
