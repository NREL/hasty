import json
from io import StringIO
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from generate.models import Site, AirHandler, TerminalUnit
from lib.helpers import HaystackBuilder
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
            print(ahus)

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


class GenerateHaystackFile(APIView):
    """
    Specifically for direct file download.  Implementation based on
    Sebastian response: https://stackoverflow.com/a/46993577/10198770
    TODO:
        1. Plan is to utilize the generate.lib.helpers functions for this
        2. This should just call one of those functions, i.e. Test() below
    """

    def get(self, request, site_id):
        site = Site.objects.get(pk=site_id)
        ahus = AirHandler.objects.filter(site_id=site_id)
        builder = HaystackBuilder(site, ahus)
        builder.build()
        cols = []
        for entity in builder.hay_json:
            for k in entity.keys():
                if {"name": k} not in cols:
                    cols.append({"name": k})
        data = {
            "meta": {
                "ver": "3.0"
            },
            "cols": cols,
            "rows": builder.hay_json
        }
        data_string = json.dumps(data)
        json_file = StringIO()
        json_file.write(data_string)
        json_file.seek(0)

        wrapper = FileWrapper(json_file)
        response = HttpResponse(wrapper, content_type='application/json')
        response['Content-Disposition'] = f"attachement; filename={site.name} haystack.json"
        return response