
from django.shortcuts import render
from django.views.generic import CreateView

from .models import HaystackPointType, BrickPointType, PointTypeMap
from .filters import BrickPointTypeFilter, HaystackPointTypeFilter, PointTypeMapFilter


# # Create your views here.
class PointMappingView(CreateView):
    template_name = 'mapp_index.html'

    def get(self, request):
        hpt = HaystackPointType.objects.all()
        bpt = BrickPointType.objects.all()
        if bpt is None and hpt is None:
            args = {
                'no_map': "No mappings have been created. Please run initial migrations and restart app."
            }
            return render(request, self.template_name, args)
        else:
            ptm = PointTypeMap.objects.all()
            map_filter = PointTypeMapFilter(request.GET)

            data = request.GET.copy()
            data['inference_version'] = '2'
            map_filter1 = PointTypeMapFilter(data)
            ptm1 = map_filter1.qs
            ptm = map_filter.qs

            bpt_filter = BrickPointTypeFilter(request.GET)
            bpt = bpt_filter.qs

            hpt_filter = HaystackPointTypeFilter(request.GET)
            hpt = hpt_filter.qs
            args = {
                'bpt': bpt,
                'hpt': hpt,
                'ptm': ptm,
                'ptm1': ptm1,
                'bpt_filter': bpt_filter,
                'hpt_filter': hpt_filter,
                'map_filter': map_filter
            }
            return render(request, self.template_name, args)
