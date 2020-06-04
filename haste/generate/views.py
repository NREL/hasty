from django.shortcuts import render
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
