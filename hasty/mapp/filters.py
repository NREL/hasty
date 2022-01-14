import django_filters

from .models import BrickPointType, HaystackPointType, PointTypeMap


class BrickPointTypeFilter(django_filters.FilterSet):
    brick_class = django_filters.CharFilter(
        field_name='brick_class', lookup_expr='iregex')

    class Meta:
        model = BrickPointType
        fields = ('brick_class', 'version',)


class HaystackPointTypeFilter(django_filters.FilterSet):
    haystack_tagset = django_filters.CharFilter(
        field_name='haystack_tagset', lookup_expr='iregex')

    class Meta:
        model = HaystackPointType
        fields = ('haystack_tagset', 'version',)


class PointTypeMapFilter(django_filters.FilterSet):
    class Meta:
        model = PointTypeMap
        fields = '__all__'
