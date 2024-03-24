from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase

from actions.models import LikeDislike

from .choices import ArticleStatus

User = get_user_model()


class ArticleTag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100, allow_unicode=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-id',)

    def save(self, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='article_set')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='article_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE)
    image = models.ImageField(upload_to='articles/', blank=True, default='no-image-available.jpg')
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    tags = models.ManyToManyField(ArticleTag, related_name='articles', blank=True)

    objects = models.Manager()

    @property
    def short_title(self) -> str:
        return self.title[:30]

    def __str__(self) -> str:
        return '{title} - {author}'.format(title=self.short_title, author=self.author)

    def get_absolute_url(self) -> str:
        return reverse_lazy('blog:blog-detail', kwargs={'slug': self.slug})

    def likes(self) -> int:
        return self.votes.likes().count()

    def dislikes(self) -> int:
        return self.votes.dislikes().count()

    def tag_list_str(self) -> str:
        return u", ".join(o.name for o in self.tags.all())

    def tag_list(self) -> list:
        return self.tags.values_list('name', flat=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-updated', '-created', 'id')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment_set', blank=True)
    content = models.TextField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_set', blank=True, null=True)
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    objects = models.Manager()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('-id',)

    def __str__(self):
        return '{user}: {article}'.format(user=self.user, article=self.article.title)

    def likes(self) -> int:
        return self.votes.likes().count()

    def dislikes(self) -> int:
        return self.votes.dislikes().count()
