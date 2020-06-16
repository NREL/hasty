from lib.helpers import Shadowfax
from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state', 'zip')


class AirHandlerForm(forms.ModelForm):
    s = Shadowfax()
    tu = s.generate_terminal_unit_types()
    tu_choices = [(h.get('id'), h.get('Description')) for h in tu]

    # Add in options for choice to be blank
    tu_choices.append(('None', 'None'))

    num_terminal_units = forms.IntegerField()
    terminal_unit_default_type = forms.ChoiceField(choices=tuple(tu_choices))

    class Meta:
        model = models.AirHandler
        fields = ("name", "heating_coil_type", "cooling_coil_type", "num_terminal_units",
                  "terminal_unit_default_type", "pre_heat_coil", "supp_heat_coil", "exhaust_fan_type",
                  "discharge_fan_type", "return_fan_type")


