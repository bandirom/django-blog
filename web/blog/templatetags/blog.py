from django import template

from blog.models import Category
from blog.serializers import CategorySerializer

register = template.Library()


@register.simple_tag
def categories_list():
    queryset = Category.objects.all()[:7]
    serializer = CategorySerializer(queryset, many=True)
    return serializer.data
