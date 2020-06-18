# Generated by Django 3.0.7 on 2020-06-17 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0004_airhandler_heating_cooling_coil_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airhandler',
            name='site_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='air_handlers', to='generate.Site'),
        ),
    ]