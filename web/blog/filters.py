from django.db.models import Q
from django_filters import rest_framework as filters


class ArticleFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
