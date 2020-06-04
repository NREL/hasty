from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state',)

class AirSystemsForm(forms.ModelForm):
    class Meta:
        model = models.AirSystems
        fields = ("name",)


class AirHandlerForm(forms.ModelForm):
    class Meta:
        model = models.AirHandler
        fields = ("name", "heating_coil_type", "cooling_coil_type")


# class TerminalUnitForm(forms.ModelForm):


    # def __init__(self, site_id, *args, **kwargs):
    #     super(AirSystemsForm, self).__init__(*args, **kwargs)
    #     self.fields['site_id'].queryset = models.Site.objects.filter(id=site_id)
