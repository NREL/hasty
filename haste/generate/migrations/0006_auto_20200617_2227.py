# Generated by Django 3.0.7 on 2020-06-17 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0005_auto_20200617_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='airhandler',
            name='discharge_air_pressure_reset_strategy',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Zone Trim and Respond'), (3, 'Average of VAV damper position signals')], default=1),
        ),
        migrations.AddField(
            model_name='airhandler',
            name='discharge_air_temperature_reset_strategy',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Outdoor air temperature reset'), (3, 'Return air temperature reset'), (4, 'Zone Trim and Respond')], default=1),
        ),
        migrations.AddField(
            model_name='airhandler',
            name='economizer_control_strategy',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Fixed dry-bulb'), (3, 'Differential dry-bulb'), (4, 'Fixed dry-bulb & differential dry-bulb'), (5, 'Fixed enthalpy & fixed dry-bulb'), (6, 'Differential enthalpy & fixed dry-bulb')], default=1),
        ),
        migrations.AddField(
            model_name='airhandler',
            name='ventilation_control_strategy',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Minimum design outside airflow control'), (3, 'DCV with zone-level CO2 sensors'), (4, 'DCV with central return sensor')], default=2),
        ),
    ]