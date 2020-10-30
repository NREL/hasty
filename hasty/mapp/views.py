
from django.shortcuts import render
from django.views.generic import CreateView

from .models import BrickPointType, HaystackPointType
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

            inf_1_data = request.GET.copy()
            inf_1_data['inference_version'] = '1'
            inf_1_filter = PointTypeMapFilter(inf_1_data)

            inf_2_data = request.GET.copy()
            inf_2_data['inference_version'] = '2'
            inf_2_filter = PointTypeMapFilter(inf_2_data)

            f1_ptm = inf_1_filter.qs
            f2_ptm = inf_2_filter.qs

            bpt_filter = BrickPointTypeFilter(request.GET)
            bpt = bpt_filter.qs

            hpt_filter = HaystackPointTypeFilter(request.GET)
            hpt = hpt_filter.qs
            args = {
                'bpt': bpt,
                'hpt': hpt,
                'ptm': f1_ptm,
                'ptm1': f2_ptm,
                'bpt_filter': bpt_filter,
                'hpt_filter': hpt_filter,
                'map_filter': inf_1_filter
            }
            return render(request, self.template_name, args)
