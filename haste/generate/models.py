from django.db import models
from lib.helpers import Shadowfax

# Create your models here.
class Site(models.Model):
    STATES = (
        ("AK", "Alaska"),
        ("AL", "Alabama"),
        ("AR", "Arkansas"),
        ("AZ", "Arizona"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DC", "District of Columbia"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("IA", "Iowa"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("MA", "Massachusetts"),
        ("MD", "Maryland"),
        ("ME", "Maine"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MO", "Missouri"),
        ("MS", "Mississippi"),
        ("MT", "Montana"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("NE", "Nebraska"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NV", "Nevada"),
        ("NY", "New York"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("PR", "Puerto Rico"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VA", "Virginia"),
        ("VT", "Vermont"),
        ("WA", "Washington"),
        ("WI", "Wisconsin"),
        ("WV", "West Virginia"),
        ("WY", "Wyoming")
    )

    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATES)
    zip = models.IntegerField()


class AirSystems(models.Model):
    name = models.CharField(max_length=50)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)


class AirHandler(models.Model):
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
    # Create the choices list on the fly
    s = Shadowfax()
    hc = s.generate_heating_coils()
    cc = s.generate_cooling_coils()
    hc_cc = s.generate_heating_cooling_coils()
    dis_fa = s.generate_discharge_fans()
    ret_fa = s.generate_return_fans()
    exh_fa = s.generate_exhaust_fans()

    hc_choices = [(h.get('id'), h.get('Description')) for h in hc]
    cc_choices = [(h.get('id'), h.get('Description')) for h in cc]
    hc_cc_choices = [(h.get('id'), h.get('Description')) for h in hc_cc]
    dis_fa_choices = [(f.get('id'), f.get('Description')) for f in dis_fa]
    ret_fa_choices = [(f.get('id'), f.get('Description')) for f in ret_fa]
    exh_fa_choices = [(f.get('id'), f.get('Description')) for f in exh_fa]

    # Add in options for choice to be blank
    hc_choices.append(('None', 'None'))
    cc_choices.append(('None', 'None'))
    hc_cc_choices.append(('None', 'None'))
    dis_fa_choices.append(('None', 'None'))
    ret_fa_choices.append(('None', 'None'))
    exh_fa_choices.append(('None', 'None'))

    name = models.CharField(max_length=50)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='air_handlers')

    # Coil Configurations
    pre_heat_coil = models.CharField(max_length=100, choices=tuple(hc_choices), default="None")
    heating_coil_type = models.CharField(max_length=100, choices=tuple(hc_choices), default="61")
    cooling_coil_type = models.CharField(max_length=100, choices=tuple(cc_choices), default="44")
    heating_cooling_coil_type = models.CharField(max_length=100, choices=tuple(hc_cc_choices), default="None")
    supp_heat_coil = models.CharField(max_length=100, choices=tuple(hc_choices), default="None")

    # Fan Configurations
    discharge_fan_type = models.CharField(max_length=100, choices=tuple(dis_fa_choices), default="5")
    return_fan_type = models.CharField(max_length=100, choices=tuple(ret_fa_choices), default="None")
    exhaust_fan_type = models.CharField(max_length=100, choices=tuple(exh_fa_choices), default="None")

    # Controls Configurations
    # Discharge temperature reset strategy
    discharge_air_temperature_reset_strategy = models.PositiveSmallIntegerField(choices=DAT_RESET_STRATEGY, default=1)
    # Discharge pressure reset strategy
    discharge_air_pressure_reset_strategy = models.PositiveSmallIntegerField(choices=DAP_RESET_STRATEGY, default=1)
    # Economizer control strategy
    economizer_control_strategy = models.PositiveSmallIntegerField(choices=ECON_STRATEGY, default=1)
    # Ventilation control strategy
    ventilation_control_strategy = models.PositiveSmallIntegerField(choices=VENTILATION_STRATEGY, default=2)

    # Damper Configurations


class ThermalZone(models.Model):
    name = models.CharField(max_length=50)


class TerminalUnit(models.Model):
    s = Shadowfax()
    # Create the choices list on the fly
    tu = s.generate_terminal_unit_types()
    tu_choices = [(h.get('id'), h.get('Description')) for h in tu]

    # Add in options for choice to be blank
    tu_choices.append(('None', 'None'))

    name = models.CharField(max_length=50)
    ahu_id = models.ForeignKey(AirHandler, on_delete=models.CASCADE)
    terminal_unit_type = models.CharField(max_length=50, choices=tuple(tu_choices))
    thermal_zone = models.OneToOneField(ThermalZone, on_delete=models.CASCADE)
