# Generated by Django 3.0.4 on 2020-06-04 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirHandler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'), ('MS', 'Mississippi'), ('MT', 'Montana'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='TerminalUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ahu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generate.AirHandler')),
            ],
        ),
        migrations.CreateModel(
            name='AirSystems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generate.Site')),
            ],
        ),
        migrations.AddField(
            model_name='airhandler',
            name='air_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generate.AirSystems'),
        ),
    ]
