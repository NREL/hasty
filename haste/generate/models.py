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
    # Create the choices list on the fly
    s = Shadowfax()
    hc = s.generate_heating_coils()
    cc = s.generate_cooling_coils()
    dis_fa = s.generate_discharge_fans()
    ret_fa = s.generate_return_fans()
    exh_fa = s.generate_exhaust_fans()

    hc_choices = [(h.get('id'), h.get('Description')) for h in hc]
    cc_choices = [(h.get('id'), h.get('Description')) for h in cc]
    dis_fa_choices = [(f.get('id'), f.get('Description')) for f in dis_fa]
    ret_fa_choices = [(f.get('id'), f.get('Description')) for f in ret_fa]
    exh_fa_choices = [(f.get('id'), f.get('Description')) for f in exh_fa]

    # Add in options for choice to be blank
    hc_choices.append(('None', 'None'))
    cc_choices.append(('None', 'None'))
    dis_fa_choices.append(('None', 'None'))
    ret_fa_choices.append(('None', 'None'))
    exh_fa_choices.append(('None', 'None'))

    name = models.CharField(max_length=50)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)

    pre_heat_coil = models.CharField(max_length=100, choices=tuple(hc_choices))
    supp_heat_coil = models.CharField(max_length=100, choices=tuple(hc_choices))
    heating_coil_type = models.CharField(max_length=100, choices=tuple(hc_choices))
    cooling_coil_type = models.CharField(max_length=100, choices=tuple(cc_choices))
    discharge_fan_type = models.CharField(max_length=100, choices=tuple(dis_fa_choices))
    return_fan_type = models.CharField(max_length=100, choices=tuple(ret_fa_choices))
    exhaust_fan_type = models.CharField(max_length=100, choices=tuple(exh_fa_choices))


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
