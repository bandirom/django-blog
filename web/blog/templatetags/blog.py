from django import template

from api.v1.blog.services import BlogService
from blog.serializers import CategorySerializer

register = template.Library()


@register.simple_tag(name='categories')
def categories_list(limit: int = 99):
    queryset = BlogService.category_queryset()[:limit]
    serializer = CategorySerializer(queryset, many=True)
    return serializer.data


@register.simple_tag(name='popular_tags')
def popular_tags() -> list:
    return BlogService.popular_tags()
