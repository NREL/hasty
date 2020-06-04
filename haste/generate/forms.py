from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state', 'zip')


class AirSystemsForm(forms.ModelForm):
    class Meta:
        model = models.AirSystems
        fields = ("name",)

class AirHandlerForm(forms.ModelForm):

    class Meta:
        model = models.AirHandler
        fields = ("name", "heating_coil_type", "cooling_coil_type")
