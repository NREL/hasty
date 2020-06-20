
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from generate.models import Site, AirHandler, TerminalUnit
from lib.helpers import HaystackBuilder, BrickBuilder
from .serializers import SiteSerializer


def index(request):
    return


# Create your views here.
class GetSites(APIView):
    """Simple test"""

    def get(self, request):
        sites = Site.objects.all()
        for site in sites:
            ahus = AirHandler.objects.filter(site_id=site.id)
            # print(ahus)

        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class GenerateHaystack(APIView):
    """
    General APIView for getting Haystack formatted JSON data.
    Same plan as below.
    """

    def get(self, request, site_id):
        data = [
            {"test": 1},
            {"test": 2}
        ]
        return Response(data)


class DownloadFile(APIView):
    """
    Specifically for direct file download.  Implementation based on
    Sebastian response: https://stackoverflow.com/a/46993577/10198770
    TODO:
        1. Plan is to utilize the generate.lib.helpers functions for this
    """

    def get(self, request, site_id):
        # import pdb; pdb.set_trace()
        print(request.query_params)
        download_type = request.query_params.get('download_type', 'haystack')
        site = Site.objects.get(pk=site_id)
        if download_type == 'haystack':
            builder = HaystackBuilder(site)
            builder.build()
            file = builder.json_file_serializer()
            response = HttpResponse(file, content_type='application/json')
            response['Content-Disposition'] = f"attachement; filename={site.name} haystack.json"
            return response
        elif download_type == 'brick':
            builder = BrickBuilder(site)
            builder.build()
            file = builder.ttl_file_serializer()

            response = HttpResponse(file, content_type='application/x-turtle')
            response['Content-Disposition'] = f"attachement; filename={site.name} brick.ttl"
            return response
