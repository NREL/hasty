import json

from django.shortcuts import render

from .models import Mapper, PointMapping
from .filters import PointMappingFilter


# Create your views here.
def mapp_index(request):
    template_name = 'mapp_index.html'
    m = Mapper.objects.first()
    pm = PointMapping.objects.filter(parent_map=m)
    filt = PointMappingFilter(request.GET, queryset=pm)
    pm = filt.qs
    for p in pm:
        p.haystack_tagset = ' '.join(json.loads(p.haystack_tagset))
    args = {
        'mapper': m,
        'point_maps': pm,
        'filter': filt
    }
    return render(request, template_name, args)
