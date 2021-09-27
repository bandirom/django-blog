from django import template
from django.db.models import Count, Q

from blog.models import Category, ArticleTag
from blog.serializers import CategorySerializer
from blog.choices import ArticleStatus
register = template.Library()


@register.simple_tag(name='categories')
def categories_list(limit: int = 99):
    queryset = Category.objects.all()[:limit]
    serializer = CategorySerializer(queryset, many=True)
    return serializer.data


@register.simple_tag(name='popular_tags')
def popular_tags() -> tuple:
    tags = ArticleTag.objects.annotate(
        articles_num=Count('tagged_article', filter=Q(tagged_article__content_object__status=ArticleStatus.ACTIVE))
    ).values('name', 'articles_num').order_by('-articles_num')[:8]
    tags = [tag for tag in tags if tag['articles_num'] > 0]
    return tags
