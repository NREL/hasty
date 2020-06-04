from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from . import forms


def index(request):
    return render(request, 'index.html')


def form(request):
    return render(request, 'form.html')


def download(request):
    return render(request, 'download.html')


class Site(CreateView):
    template_name = 'site.html'

    def get(self, request):
        form = forms.AirSystemForm()
        args = {'form': form}
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
            new_form = forms.AirSystemForm()
            site_def = form_result.save()
            args = {'form': new_form}
            return redirect('site')


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
