import json
from io import StringIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib import messages
from . import forms
from . import models
from lib.helpers import Shadowfax
from lib.helpers import HaystackBuilder


def index(request):
    sites = models.Site.objects.all()
    for site in sites:
        ahus = models.AirHandler.objects.filter(site_id=site.id)

    args = {
        'sites': sites
    }
    return render(request, 'index.html', args)


def data_view(request, site_id):

    site = models.Site.objects.get(pk=site_id)
    args = {
        'site': site
    }
    return render(request, 'data_view.html', args)


class Site(CreateView):
    template_name = 'site.html'

    def get(self, request, site_id):
        s = Shadowfax()
        site = models.Site.objects.get(id=site_id)
        ahu_info = []
        ahus = models.AirHandler.objects.filter(site_id=site_id)
        for ahu in ahus:
            ahu_info.append(s.ahu_summary_info(ahu))
        air_handler_form = forms.AirHandlerForm()
        args = {
            'air_handler_form': air_handler_form,
            'site': site,
            'ahus': ahu_info
        }
        return render(request, self.template_name, args)

    def post(self, request, site_id):
        if site_id is not None:
            site = get_object_or_404(models.Site, id=site_id)
        if 'create_air_handler' in request.POST:
            print(request.POST)
            form_result = forms.AirHandlerForm(request.POST)
            if form_result.is_valid():
                ahu_def = form_result.save(commit=False)
                ahu_def.site_id = site
                ahu_def.save()
                ntu = int(form_result.cleaned_data['num_terminal_units'])
                tudt = form_result.cleaned_data['terminal_unit_default_type']
                s = Shadowfax()
                terminal_unit_types = s.generate_terminal_unit_types()

                for tu in terminal_unit_types:
                    if tudt == tu["id"]:
                        category = tu["category"]
                for i in range(1, ntu + 1):
                    new_tu = models.TerminalUnit(name=f"{category}-{i:03d}", terminal_unit_type=tudt, ahu_id=ahu_def)
                    new_tz = models.ThermalZone(name=f"Zone-{i:03d}")
                    new_tz.save()
                    new_tu.thermal_zone = new_tz
                    new_tu.save()

                return redirect('site.ahu', site_id=site_id, ahu_id=ahu_def.id)
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
        tus = models.TerminalUnit.objects.filter(ahu_id=ahu_id)
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
            tus = models.TerminalUnit.objects.filter(ahu_id=ahu_id)
            for tu in tus:
                if tu.name in data.keys():
                    new_name = data.get(tu.name, False)
                    tu.name = new_name
                    tu.terminal_unit_type = data.get('terminal_unit')
                    tu.save()

            return redirect('site.ahu', site_id=site_id, ahu_id=ahu_id)

