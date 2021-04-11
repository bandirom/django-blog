from django_filters import rest_framework as filters
from django.db.models import Q


class CharFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ArticleFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
