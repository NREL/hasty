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



    # def save(self, commit=True):
    #     ntu = int(self.cleaned_data['num_terminal_units'])
    #     tudt = self.cleaned_data['terminal_unit_default_type']
    #     terminal_unit_types = generate_terminal_unit_types()
    #
    #     for tu in terminal_unit_types:
    #         if tudt == tu["id"]:
    #             category = tu["category"]
    #     for i in range(1, ntu + 1):
    #         new = models.TerminalUnit(name=f"{category}-{i:03d}", terminal_unit_type=tudt, ahu_id=)
    #     print(self.cleaned_data['num_terminal_units'])
    #     print(self.cleaned_data['terminal_unit_default_type'])
    #     return super(AirHandlerForm, self).save(commit=commit)
