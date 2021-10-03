from django import template

from blog.serializers import CategorySerializer
from blog.services import BlogService

register = template.Library()


@register.simple_tag(name='categories')
def categories_list(limit: int = 99):
    queryset = BlogService.category_queryset()[:limit]
    serializer = CategorySerializer(queryset, many=True)
    return serializer.data


@register.simple_tag(name='popular_tags')
def popular_tags() -> list:
    return BlogService.popular_tags()
