import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from . import forms
from . import models
from lib.helpers import Shadowfax, BrickBuilder, file_proccessing


class Index(CreateView):

    def get(self, request):
        sites = models.Site.objects.all()
        ahus = models.AirHandler.objects.all()

        args = {
            'sites': sites,
            'ahus': ahus
        }
        return render(request, 'index.html', args)

    def post(self, request):

        file = request.FILES['file']
        file_proccessing(file)
        print(file)

        sites = models.Site.objects.all()
        ahus = models.AirHandler.objects.all()

        args = {
            'sites': sites,
            'ahus': ahus
        }

        return render(request, 'index.html', args)


def data_view(request, site_id):

    site = models.Site.objects.get(pk=site_id)
    args = {
        'site': site
    }
    if request.GET['download_type'] == 'haystack':
        return render(request, 'data_view.html', args)
    elif request.GET['download_type'] == 'brick':
        builder = BrickBuilder(site)
        builder.build()
        file = builder.ttl_file_serializer()
        url = 'https://viewer.brickschema.org/upload'

        return HttpResponseRedirect(url)


class Site(CreateView):
    template_name = 'site.html'

    def get(self, request, site_id):
        s = Shadowfax()
        site = models.Site.objects.get(id=site_id)
        ahu_info = []
        ahus = models.AirHandler.objects.filter(site_id=site_id)
        # tus = models.TerminalUnit.objects.filter(ahu_id=)
        count = 0
        for ahu in ahus:
            tus = ahu.feeds.all()
            count += tus.count()
        air_handler_form = forms.AirHandlerForm()
        args = {
            'air_handler_form': air_handler_form,
            'site': site,
            'ahus': ahus,
            'tus_count': count
        }
        return render(request, self.template_name, args)

    def post(self, request, site_id):
        if site_id is not None:
            site = get_object_or_404(models.Site, id=site_id)
        if 'create_air_handler' in request.POST:
            form_result = forms.AirHandlerForm(request.POST)
            if form_result.is_valid():
                form_result.generate_ahu(site.id)
                form_result.generate_all_components()
                form_result.generate_terminal_units_and_thermal_zones()
                form_result.generate_base_ahu_points()
                return redirect('site.ahu', site_id=site_id, ahu_id=form_result.ahu_model.id)
            else:
                args = {
                    'form': form_result,
                    'site': site
                }
                return render(request, 'air_handler_errors.html', args)

        elif 'create_hot_water_system' in request.POST:
            pass
        elif 'create_chilled_water_system' in request.POST:
            pass
        else:
            pass


class CreateSite(CreateView):
    template_name = 'add_site.html'

    def get(self, request):
        form = forms.SiteForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form_result = forms.SiteForm(request.POST)
        if form_result.is_valid():
            site_def = form_result.save()
            return redirect('site', site_id=site_def.id)


class AirHandler(CreateView):
    template_name = 'air_handler.html'

    def get(self, request, site_id, ahu_id):
        s = Shadowfax()
        tu_info = []
        tu_types = s.generate_terminal_unit_types()
        site = models.Site.objects.get(id=site_id)
        ahu = models.AirHandler.objects.get(id=ahu_id)
        tus = ahu.feeds.all()
        for tu in tus:
            tu_info.append(s.terminal_unit_summary_info(tu))
        args = {
            'site': site,
            'ahu': ahu,
            'terminal_units': tu_info,
            'terminal_unit_types': tu_types
        }
        return render(request, self.template_name, args)

    def post(self, request, site_id, ahu_id):
        if 'update_terminal_unit' in request.POST:
            data = request.POST
            key = next(iter(data))
            tu = models.TerminalUnit.objects.get(id=key)
            new_name = data.get(key, False)
            tu.name = new_name
            tu.lookup_id = data.get('terminal_unit')
            tu.save()

            return redirect('site.ahu', site_id=site_id, ahu_id=ahu_id)

