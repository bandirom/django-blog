from django.db.models import Count, Prefetch, Q, QuerySet
from rest_framework.exceptions import ValidationError
from slugify import slugify

from api.v1.actions.services import LikeQueryService
from api.v1.blog.types import CreateArticleT
from blog.choices import ArticleStatus
from blog.models import Article, ArticleTag, Category, Comment

from main.decorators import except_shell
from main.models import UserType


class BlogQueryService:
    @staticmethod
    def get_queryset() -> QuerySet[Article]:
        return Article.objects.all()

    def get_active_articles(self) -> QuerySet[Article]:
        return self.get_queryset().filter(status=ArticleStatus.ACTIVE)

    def get_articles(self, user: UserType) -> QuerySet[Article]:
        return (
            self.get_active_articles()
            .select_related('category', 'author')
            .prefetch_related('tags')
            .annotate(comments_count=Count('comment_set'), like_status=LikeQueryService.like_annotate(user))
        )

    @except_shell((Article.DoesNotExist,), raise_404=True)
    def get_article_by_slug(self, slug: str, user) -> Article:
        return self.get_articles(user).get(slug=slug)


class CommentQueryService:
    @staticmethod
    def get_queryset() -> QuerySet[Comment]:
        return Comment.objects.all()

    def comments_by_article_slug(self, article_slug: str, user: UserType) -> QuerySet[Comment]:
        return (
            self.get_queryset()
            .filter(article__slug=article_slug, parent__isnull=True)
            .select_related('user')
            .prefetch_related(
                Prefetch('parent_set', queryset=Comment.objects.all().select_related('user')),
            )
            .annotate(like_status=LikeQueryService.like_annotate(user))
        )

    @staticmethod
    def is_valid_comment_parent(parent_id: int, article: Article) -> bool:
        return Comment.objects.filter(id=parent_id, article=article, parent__isnull=True).exists()


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


class CategoryQueryService:
    @staticmethod
    def category_queryset() -> QuerySet[Category]:
        return Category.objects.all()

    @staticmethod
    def get_comments_queryset() -> QuerySet[Comment]:
        return (
            Comment.objects.select_related('user', 'article', 'parent')
            .filter(article__status=ArticleStatus.ACTIVE)
            .order_by('id')
        )

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


class CreateArticleService:

    @staticmethod
    def _get_slug(value: str) -> str:
        return slugify(value)

    @staticmethod
    def is_article_slug_exist(slug: str) -> bool:
        return Article.objects.filter(slug=slug).exists()

    def create_article(self, author: 'UserType', article_data: CreateArticleT) -> Article:
        slug = self._get_slug(article_data['title'])
        if self.is_article_slug_exist(slug):
            raise ValidationError('Article with this title already exists')
        return Article.objects.create(author=author, slug=slug, **article_data)
