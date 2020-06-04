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

def site(request):
    return render(request, 'site.html')


class CreateSite(CreateView):
    template_name = 'add_site.html'

    def get(self, request):
        form = forms.SiteForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form_result = forms.SiteForm(request.POST)
        if form_result.is_valid():
            site_def = form.save(commit=False)
            site_def.save()

            return redirect('site.html', site_def=site_def)