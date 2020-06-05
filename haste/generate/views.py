from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from . import forms
from . import models


def index(request):
    sites = models.Site.objects.all()
    args = {
        'sites': sites
    }
    return render(request, 'index.html', args)


def form(request):
    return render(request, 'form.html')


def download(request):
    return render(request, 'download.html')


class Site(CreateView):
    template_name = 'site.html'

    def get(self, request, site_id):
        site = models.Site.objects.get(id=site_id)
        # print(site[0].id)
        air_sys_form = forms.AirSystemsForm()
        air_handle_form = forms.AirHandlerForm()
        args = {
            'air_sys_form': air_sys_form,
            'air_handle_form': air_handle_form,
            'site': site
        }
        return render(request, self.template_name, args)

    def post(self, request):
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


class CreateAirSystem(CreateView):
    template_name = 'add_air_system.html'

    def get(self, request):
        form = forms.AirSystemForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form_result = forms.AirSystemForm(request.POST)
        if form_result.is_valid():
            air_sys_def = form_result.save()
            args = {'air_sys': air_sys_def}
            # site_def.save()

            # return render(request, 'site.html', args)
