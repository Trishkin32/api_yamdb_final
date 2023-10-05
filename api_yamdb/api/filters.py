from django_filters.rest_framework import (
    CharFilter,
    FilterSet,
    NumberFilter
)


class TitleFilter(FilterSet):
    """Фильтр для Title."""

    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year')  # При удалении фильтра -
    # не проходит pytest
