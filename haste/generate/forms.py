from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state', 'zip')


class AirSystemForm(forms.ModelForm):
    class Meta:
        model = models.AirSystems
        fields = ('name',)


class AirHandlerForm(forms.ModelForm):
    class Meta:
        model = models.AirHandler
        fields = ('name',)
