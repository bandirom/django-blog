from django.conf import settings

from .models import Category, Article, Comment


class BlogService:

    @staticmethod
    def category_queryset():
        return Category.objects.all()

    @staticmethod
    def article_queryset():
        return Article.objects.all()
