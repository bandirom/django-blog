from functools import reduce
from operator import and_

from django.db.models import Q
from django_filters import rest_framework as filters

from main.filters import ListCharFilter


class ArticleFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    tags = ListCharFilter(method='tags_filter')

    def search_filter(self, queryset, name: str, value: str):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def tags_filter(self, queryset, name: str, value: list[str]):
        tag_queries = [Q(tags__slug=tag) for tag in value]
        # Use the reduce function to combine the Q objects with the 'and' operator
        combined_query = reduce(and_, tag_queries)
        return queryset.filter(combined_query)
