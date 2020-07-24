import django_filters

from .models import PointMapping

# class BetterCharFilter()


class PointMappingFilter(django_filters.FilterSet):
    haystack_tagset = django_filters.CharFilter(field_name='haystack_tagset', lookup_expr='iregex')
    brick_class = django_filters.CharFilter(field_name='brick_class', lookup_expr='iregex')

    class Meta:
        model = PointMapping
        fields = ('haystack_tagset', 'brick_class')
