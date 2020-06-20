from uuid import uuid4

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from lib.helpers import Shadowfax

SHADOW = Shadowfax()


# Create your models here.
class Point(models.Model):
    choices = SHADOW.generate_points()
    ch = [(h.get('id'), h.get('Final Typing Tagset')) for h in choices]

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
    lookup_id = models.CharField(max_length=100, choices=ch)
    tagset = models.CharField(max_length=200, default=None, null=True)
    brick_class = models.CharField(max_length=100, default=None, null=True)

    # https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#django.contrib.contenttypes.models.ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    is_point_of = GenericForeignKey('content_type', 'object_id')


class Component(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=50, null=True)
    tagset = models.CharField(max_length=200, default=None, null=True)
    brick_class = models.CharField(max_length=100, default=None, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True)
    is_part_of = GenericForeignKey('content_type', 'object_id')
    has_part = GenericRelation('Component')

    has_points = GenericRelation(Point)


class HeatingCoil(Component):
    _ = SHADOW.generate_heating_coils()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, default="61", null=True, blank=True)


class CoolingCoil(Component):
    _ = SHADOW.generate_cooling_coils()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, default="44", null=True, blank=True)


class PreHeatCoil(Component):
    _ = SHADOW.generate_heating_coils()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, null=True, blank=True)


class SupplementaryHeatingCoil(Component):
    _ = SHADOW.generate_heating_coils()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, null=True, blank=True)


class DischargeFan(Component):
    _ = SHADOW.generate_discharge_fans()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, null=True, blank=True)


class ReturnFan(Component):
    _ = SHADOW.generate_return_fans()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, null=True, blank=True)


class ExhaustFan(Component):
    _ = SHADOW.generate_exhaust_fans()
    choices = [(h.get('id'), h.get('Description')) for h in _]
    lookup_id = models.CharField(max_length=100, choices=choices, null=True, blank=True)


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

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATES)
    zip = models.IntegerField()


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

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='air_handlers')
    tagset = models.CharField(max_length=200, default=None, null=True)
    brick_class = models.CharField(max_length=100, default=None, null=True)

    # Controls Configurations
    discharge_air_temperature_reset_strategy = models.PositiveSmallIntegerField(choices=DAT_RESET_STRATEGY, default=1)
    discharge_air_pressure_reset_strategy = models.PositiveSmallIntegerField(choices=DAP_RESET_STRATEGY, default=1)
    economizer_control_strategy = models.PositiveSmallIntegerField(choices=ECON_STRATEGY, default=1)
    ventilation_control_strategy = models.PositiveSmallIntegerField(choices=VENTILATION_STRATEGY, default=2)

    has_part = GenericRelation(Component)
    has_point = GenericRelation(Point)


class ThermalZone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=50)
    tagset = models.CharField(max_length=200, default=None, null=True)
    brick_class = models.CharField(max_length=100, default=None, null=True)

    has_point = GenericRelation(Point)


class TerminalUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    s = Shadowfax()
    # Create the choices list on the fly
    tu = s.generate_terminal_unit_types()
    tu_choices = [(h.get('id'), h.get('Description')) for h in tu]

    # Add in options for choice to be blank
    tu_choices.append(('None', 'None'))

    name = models.CharField(max_length=50)
    ahu_id = models.ForeignKey(AirHandler, on_delete=models.CASCADE)
    lookup_id = models.CharField(max_length=50, choices=tuple(tu_choices))

    tagset = models.CharField(max_length=200, default=None, null=True)
    brick_class = models.CharField(max_length=100, default=None, null=True)
    thermal_zone = models.OneToOneField(ThermalZone, on_delete=models.CASCADE)

    has_part = GenericRelation(Component)
    has_point = GenericRelation(Point)
