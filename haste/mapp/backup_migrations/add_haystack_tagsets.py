# Generated by Django 3.0.7 on 2020-07-31 01:59
import os
from bs4 import BeautifulSoup
from django.db import migrations


def generate_haystack_tagsets(apps, schema_editor):
    hv = "3.9.9"
    HaystackPointType = apps.get_model('mapp', 'HaystackPointType')
    HaystackMarkerTag = apps.get_model('mapp', 'HaystackMarkerTag')
    p = os.path.join(os.getcwd(), f"mapp/resources/haystack/{hv}/index-pointProtos.html")
    with open(p, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, features="html.parser")
    all_protos = soup.find_all('th')

    # Generate a list of sets
    all_protos = [p.a.text.replace(' ', '-') for p in all_protos]
    for proto in all_protos:
        hpt = HaystackPointType(haystack_tagset=proto)
        hpt.save()
        for tag in proto.split('-'):
            haystack_marker_model = HaystackMarkerTag.objects.filter(tag=tag, version__version=hv)
            if len(haystack_marker_model) == 1:
                hpt.tags.add(haystack_marker_model[0])
            elif len(haystack_marker_model) == 0:
                print(f"Haystack tag: {tag} is not a marker tag in version {hv}")
                print(f"A record for following proto will not be created: {proto}")
                hpt.delete()
                break
            else:
                print(f"Haystack tag: {tag} has multiple tags in version {hv}")
                print(f"A record for following proto will not be created: {proto}")
                hpt.delete()
                break


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0002_auto_20200731_0155'),
    ]

    operations = [
        migrations.RunPython(generate_haystack_tagsets)
    ]
