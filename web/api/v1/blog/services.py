from typing import List

from django.db.models import Count, Prefetch, Q, QuerySet

from blog.choices import ArticleStatus
from blog.models import Article, ArticleTag, Category, Comment

from main.decorators import except_shell


class BlogQueryService:
    @staticmethod
    def get_queryset() -> QuerySet[Article]:
        return Article.objects.all()

    def get_active_articles(self) -> QuerySet[Article]:
        return self.get_queryset().filter(status=ArticleStatus.ACTIVE)

    def get_articles(self) -> QuerySet[Article]:
        return (
            self.get_active_articles()
            .select_related('category', 'author')
            .prefetch_related('tags')
            .annotate(comments_count=Count('comment_set'))
        )

    @except_shell((Article.DoesNotExist,), raise_404=True)
    def get_article_by_slug(self, slug: str) -> Article:
        return self.get_articles().get(slug=slug)


class CommentQueryService:
    @staticmethod
    def get_queryset() -> QuerySet[Comment]:
        return Comment.objects.all()

    def comments_by_article_slug(self, article_slug: str) -> QuerySet[Comment]:
        return self.get_queryset().filter(article__slug=article_slug)


class TagQueryService:
    @staticmethod
    def get_queryset() -> QuerySet[ArticleTag]:
        return ArticleTag.objects.all()

    def popular_tags(self) -> QuerySet[dict]:
        tags = (
            self.get_queryset()
            .annotate(articles_num=Count('tagged_article', filter=Q(article_tags__status=ArticleStatus.ACTIVE)))
            .values('name', 'slug', 'articles_num')
            .filter(articles_num__gt=0)
            .order_by('-articles_num')[:8]
        )
        return tags


class BlogService:
    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    def get_active_articles(self) -> QuerySet[Article]:
        return (
            Article.objects.select_related('category', 'author')
            .prefetch_related('tags')
            .filter(status=ArticleStatus.ACTIVE)
            .annotate(comments_count=Count('comment_set'))
        )

    @staticmethod
    def get_comments_queryset() -> QuerySet[Comment]:
        return (
            Comment.objects.select_related('user', 'article', 'parent')
            .filter(article__status=ArticleStatus.ACTIVE)
            .order_by('id')
        )

    @staticmethod
    def is_valid_comment_parent(parent_id: int, article: Article) -> bool:
        return Comment.objects.filter(id=parent_id, article=article, parent__isnull=True).exists()

    @staticmethod
    def get_article_comments(article_id: int):
        return Comment.objects.filter(article_id=article_id, parent__isnull=True)

    @except_shell((Article.DoesNotExist,))
    def get_article(self, article_id: int) -> Article:
        return Article.objects.select_related('category').prefetch_related('comment_set').get(id=article_id)

    @staticmethod
    @except_shell((Comment.DoesNotExist,))
    def get_comment(comment_id: int):
        return Comment.objects.get(id=comment_id)

    @staticmethod
    def is_article_slug_exist(title: str) -> bool:
        return Article.objects.filter(slug=Article.get_slug(title)).exists()
