from typing import List

from django.db.models import Count, Prefetch, Q, QuerySet

from blog.choices import ArticleStatus
from main.decorators import except_shell


from blog.models import Article, ArticleTag, Category, Comment


class BlogService:
    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    def get_active_articles(self) -> QuerySet[Article]:
        comment_prefetch = Prefetch(
            'comment_set', queryset=BlogService.get_comments_queryset(), to_attr='comments'
        )
        return (
            Article.objects.select_related('category', 'author')
            .prefetch_related(comment_prefetch)
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

    @except_shell((Article.DoesNotExist,))
    def get_article_by_slug(self, slug: str) -> Article:
        return self.get_active_articles().get(slug=slug)

    @staticmethod
    @except_shell((Comment.DoesNotExist,))
    def get_comment(comment_id: int):
        return Comment.objects.get(id=comment_id)

    @staticmethod
    def is_article_slug_exist(title: str) -> bool:
        return Article.objects.filter(slug=Article.get_slug(title)).exists()

    @staticmethod
    def popular_tags() -> List[dict]:
        tags = (
            ArticleTag.objects.annotate(
                articles_num=Count('tagged_article', filter=Q(article_tags__status=ArticleStatus.ACTIVE))
            )
            .values('name', 'articles_num')
            .order_by('-articles_num')[:8]
        )
        tags = [tag for tag in tags if tag['articles_num'] > 0]
        return tags
