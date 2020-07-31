
from django.shortcuts import render
from django.views.generic import CreateView

from .models import PointTypeMap
# from .filters import PointMappingFilter, MapperFilter


# # Create your views here.
class PointMappingView(CreateView):
    template_name = 'mapp_index.html'

    def get(self, request):
        m = PointTypeMap.objects.first()
        if m is None:
            args = {
                'no_map': "No mappings have been created. Please run initial migrations and restart app."
            }
            return render(request, self.template_name, args)
#             #
#             # return HttpResponse("There are no Mappings in the Database.  Please follow the directions in the README to "
#             #                     "add mappings for atleast 1 version of Haystack, Brick, and py-brickschema")
#         m.haystack_version
#         m.brick_version
#         m.brick_inference_version
#         m_all = Mapper.objects.all()
#         hv_all = [mm.haystack_version for mm in m_all]
#         bv_all = [mm.brick_version for mm in m_all]
#         biv_all = [mm.brick_inference_version for mm in m_all]
#
#         map_filter = MapperFilter(request.GET)
#         m = map_filter.qs[0]
#         pm = PointMapping.objects.filter(parent_map=m)
#         pm_filter = PointMappingFilter(request.GET, queryset=pm)
#         pm = pm_filter.qs
#         for p in pm:
#             p.haystack_tagset = ' '.join(json.loads(p.haystack_tagset))
#         args = {
#             'hv_all': hv_all,
#             'bv_all': bv_all,
#             'biv_all': biv_all,
#             'mapper': m,
#             'point_maps': pm,
#             'pm_filter': pm_filter,
#             'map_filter': map_filter
#         }
#         return render(request, self.template_name, args)
