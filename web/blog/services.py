from django.conf import settings
from django.db.models import Count, QuerySet, Prefetch

from main.decorators import except_shell
from .choices import ArticleStatus
from .models import Category, Article, Comment


class BlogService:

    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    @staticmethod
    def get_active_articles() -> QuerySet[Article]:
        comment_prefetch = Prefetch('comment_set', queryset=BlogService.get_comments_queryset(), to_attr='comments')
        return (Article.objects
                .select_related('category', 'author')
                .prefetch_related(comment_prefetch)
                .filter(status=ArticleStatus.ACTIVE)
                .annotate(comments_count=Count('comment_set'))
                )

    @staticmethod
    def get_comments_queryset() -> QuerySet[Comment]:
        return Comment.objects.select_related('user', 'article', 'parent').filter(article__status=ArticleStatus.ACTIVE)

    @staticmethod
    def is_valid_comment_parent(parent_id: int, article: Article) -> bool:
        return Comment.objects.filter(id=parent_id, article=article, parent__isnull=True).exists()

    @staticmethod
    def get_article_comments(article_id: int):
        return Comment.objects.filter(article_id=article_id, parent__isnull=True)

    @staticmethod
    @except_shell((Article.DoesNotExist,))
    def get_article(article_id: int):
        return Article.objects.select_related('category').prefetch_related('comment_set').get(id=article_id)

    @staticmethod
    @except_shell((Comment.DoesNotExist,))
    def get_comment(comment_id: int):
        return Comment.objects.get(id=comment_id)

    @staticmethod
    def is_article_slug_exist(title: str) -> bool:
        return Article.objects.filter(slug=Article.get_slug(title)).exists()
