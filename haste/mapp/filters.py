import django_filters

from .models import PointMapping, Mapper


class PointMappingFilter(django_filters.FilterSet):
    haystack_tagset = django_filters.CharFilter(field_name='haystack_tagset', lookup_expr='iregex')
    brick_class = django_filters.CharFilter(field_name='brick_class', lookup_expr='iregex')

    class Meta:
        model = PointMapping
        fields = ('haystack_tagset', 'brick_class')


class MapperFilter(django_filters.FilterSet):
    brick_inference_version = django_filters.ChoiceFilter(choices=list((m.brick_inference_version, m.brick_inference_version) for m in Mapper.objects.all()))

    class Meta:
        model = Mapper
        fields = ('haystack_version', 'brick_version', 'brick_inference_version')
