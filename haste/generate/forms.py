import json

from lib.helpers import Shadowfax, is_false, is_number, json_dump_tags_from_string
from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state', 'zip')


class AirHandlerForm(forms.Form):
    s = Shadowfax()

    DAT_RESET_STRATEGY = (
        (1, "None"),
        (2, "Outdoor air temperature reset"),
        (3, "Return air temperature reset"),
        (4, "Zone Trim and Respond")
    )
    DAP_RESET_STRATEGY = (
        (1, "None"),
        (2, "Zone Trim and Respond"),
        (3, "Average of VAV damper position signals")
    )
    ECON_STRATEGY = (
        (1, "None"),
        (2, "Fixed dry-bulb"),
        (3, "Fixed enthalpy"),
        (4, "Differential dry-bulb"),
        (5, "Differential enthalpy"),
        (6, "Fixed dry-bulb & differential dry-bulb"),
        (7, "Fixed enthalpy & fixed dry-bulb"),
        (8, "Differential enthalpy & fixed dry-bulb")
    )
    VENTILATION_STRATEGY = (
        (1, "None"),
        (2, "Minimum design outside airflow control"),
        (3, "DCV with zone-level CO2 sensors"),
        (4, "DCV with central return sensor")
    )

    tu = s.generate_terminal_unit_types()
    hc = s.generate_heating_coils()
    cc = s.generate_cooling_coils()
    hc_cc = s.generate_heating_cooling_coils()
    dis_fa = s.generate_discharge_fans()
    ret_fa = s.generate_return_fans()
    exh_fa = s.generate_exhaust_fans()

    tu_choices = [(h.get('id'), h.get('Description')) for h in tu]
    hc_choices = [(h.get('id'), h.get('Description')) for h in hc]
    cc_choices = [(h.get('id'), h.get('Description')) for h in cc]
    hc_cc_choices = [(h.get('id'), h.get('Description')) for h in hc_cc]
    dis_fa_choices = [(f.get('id'), f.get('Description')) for f in dis_fa]
    ret_fa_choices = [(f.get('id'), f.get('Description')) for f in ret_fa]
    exh_fa_choices = [(f.get('id'), f.get('Description')) for f in exh_fa]

    # Add in options for choice to be blank
    tu_choices.append((False, 'None'))
    hc_choices.append((False, 'None'))
    cc_choices.append((False, 'None'))
    hc_cc_choices.append((False, 'None'))
    dis_fa_choices.append((False, 'None'))
    ret_fa_choices.append((False, 'None'))
    exh_fa_choices.append((False, 'None'))

    name = forms.CharField(max_length=50)
    pre_heat_coil = forms.ChoiceField(choices=hc_choices)
    heating_coil_type = forms.ChoiceField(choices=hc_choices)
    cooling_coil_type = forms.ChoiceField(choices=cc_choices)
    heating_cooling_coil_type = forms.ChoiceField(choices=hc_cc_choices)
    supp_heat_coil = forms.ChoiceField(choices=hc_choices)

    discharge_fan_type = forms.ChoiceField(choices=dis_fa_choices)
    return_fan_type = forms.ChoiceField(choices=ret_fa_choices)
    exhaust_fan_type = forms.ChoiceField(choices=exh_fa_choices)

    terminal_unit_default_type = forms.ChoiceField(choices=tu_choices)
    num_terminal_units = forms.IntegerField()

    discharge_air_temperature_reset_strategy = forms.ChoiceField(choices=DAT_RESET_STRATEGY)
    discharge_air_pressure_reset_strategy = forms.ChoiceField(choices=DAP_RESET_STRATEGY)
    economizer_control_strategy = forms.ChoiceField(choices=ECON_STRATEGY)
    ventilation_control_strategy = forms.ChoiceField(choices=VENTILATION_STRATEGY)

    def __init__(self, *args, **kwargs):
        super(AirHandlerForm, self).__init__(*args, **kwargs)
        self.sf = Shadowfax()
        self.site_model = None
        self.ahu_model = None

    def generate_ahu(self, site_id):
        """
        Do this first
        :param site_id:
        :return:
        """
        self.site_model = models.Site.objects.get(id=site_id)
        ahu = models.AirHandler(name=self.cleaned_data['name'],
                                site_id=self.site_model,
                                discharge_air_temperature_reset_strategy=self.cleaned_data[
                                    'discharge_air_temperature_reset_strategy'],
                                discharge_air_pressure_reset_strategy=self.cleaned_data[
                                    'discharge_air_pressure_reset_strategy'],
                                economizer_control_strategy=self.cleaned_data['economizer_control_strategy'],
                                ventilation_control_strategy=self.cleaned_data['ventilation_control_strategy'],
                                )
        ahu.save()
        self.ahu_model = ahu

    def generate_all_components(self):
        """
        Wrapper to create all other components.
        :return:
        """
        self.generate_hc()
        self.generate_cc()
        self.generate_phc()
        self.generate_shc()
        self.generate_df()
        self.generate_rf()
        self.generate_ef()

    def generate_hc(self):
        hc_type = self.cleaned_data['heating_coil_type']
        if not is_false(hc_type):
            name, dis, tags = self.doer(hc_type)
            hc = models.HeatingCoil(
                name=name,
                lookup_id=hc_type,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            hc.save()

    def generate_cc(self):
        cc_type = self.cleaned_data['cooling_coil_type']
        if not is_false(cc_type):
            name, dis, tags = self.doer(cc_type)
            cc = models.CoolingCoil(
                name=name,
                lookup_id=cc_type,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def generate_phc(self):
        t = self.cleaned_data['pre_heat_coil']
        if not is_false(t):
            name, dis, tags = self.doer(t)
            cc = models.PreHeatCoil(
                name=name,
                lookup_id=t,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def generate_shc(self):
        t = self.cleaned_data['supp_heat_coil']
        if not is_false(t):
            name, dis, tags = self.doer(t)
            cc = models.SupplementaryHeatingCoil(
                name=name,
                lookup_id=t,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def generate_df(self):
        t = self.cleaned_data['discharge_fan_type']
        if not is_false(t):
            name, dis, tags = self.doer(t)
            cc = models.DischargeFan(
                name=name,
                lookup_id=t,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def generate_rf(self):
        t = self.cleaned_data['return_fan_type']
        if not is_false(t):
            name, dis, tags = self.doer(t)
            cc = models.ReturnFan(
                name=name,
                lookup_id=t,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def generate_ef(self):
        t = self.cleaned_data['exhaust_fan_type']
        if not is_false(t):
            name, dis, tags = self.doer(t)
            cc = models.ExhaustFan(
                name=name,
                lookup_id=t,
                short_description=dis,
                is_part_of=self.ahu_model,
                tags=tags
            )
            cc.save()

    def doer(self, t):
        temp = self.sf.df_components[self.sf.df_components['id'] == t]
        n = f"{self.ahu_model.name} {temp['Description'].values[0]}"
        dis = temp['Description'].values[0]
        tags = temp['Final Tagset'].values[0]
        return_tags = json_dump_tags_from_string(tags)
        return n, dis, return_tags

    def generate_base_ahu_points(self):
        # This is a dummy implementation.
        # TODO: Make robust
        ahu_id = '63'
        self.gen_component_point_set(self.ahu_model, ahu_id)

    def gen_component_point_set(self, component, component_id):
        comp_points = self.sf.df_component_points[self.sf.df_component_points['On Type ID'] == component_id]
        for ind in comp_points.index:
            t = json_dump_tags_from_string(comp_points['Point Tagset'][ind])
            p = models.Point(
                name=f"{component.name} {comp_points['Point Tagset'][ind]}",
                point_type=comp_points['Add Point ID'][ind],
                tags=t,
                is_point_of=component
            )
            p.save()
