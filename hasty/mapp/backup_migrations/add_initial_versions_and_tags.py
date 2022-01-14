# Generated by Django 3.0.7 on 2020-07-30 21:14
import os

from django.db import migrations

from brickschema.graph import Graph as BrickGraph
from brickschema.namespaces import BRICK
from rdflib import Namespace, Graph, RDF


PH = Namespace("https://project-haystack.org/def/ph/3.9.9#")
PHICT = Namespace("https://project-haystack.org/def/phIct/3.9.9#")
PHSCIENCE = Namespace("https://project-haystack.org/def/phScience/3.9.9#")
PHIOT = Namespace("https://project-haystack.org/def/phIoT/3.9.9#")


def generate_brick_version(apps, schema_editor):
    bv = '1.1'
    BrickVersion = apps.get_model('mapp', 'BrickVersion')
    b = BrickVersion(version=bv)
    b.save()


def generate_haystack_version(apps, schema_editor):
    hv = '3.9.9'
    HaystackVersion = apps.get_model('mapp', 'HaystackVersion')
    b = HaystackVersion(version=hv)
    b.save()


def generate_haystack_marker_tags(apps, schema_editor):
    hv = '3.9.9'
    HaystackVersion = apps.get_model('mapp', 'HaystackVersion')
    HaystackMarkerTag = apps.get_model('mapp', 'HaystackMarkerTag')
    haystack_version_model = HaystackVersion.objects.get(version=hv)
    p = os.path.join(os.getcwd(), f"mapp/resources/haystack/{hv}/defs.ttl")

    g = Graph()
    g.bind("ph", PH)
    g.bind("phict", PHICT)
    g.bind("phscience", PHSCIENCE)
    g.bind("phiot", PHIOT)
    g.parse(p, format="ttl")

    # We use everything that is a subclass of a marker, else we wouldn't
    # get things that are substances, phenomena, etc.
    q = "SELECT ?m WHERE { ?m rdfs:subClassOf* ph:marker}"
    match = g.query(q)

    all_tags = [m[0] for m in match]
    for tag in all_tags:
        ns, t = tag.split("#")
        t = HaystackMarkerTag(
            tag=t,
            version=haystack_version_model,
            namespace=ns)
        t.save()


def generate_brick_tags(apps, schema_editor):
    bv = '1.1'
    BrickVersion = apps.get_model('mapp', 'BrickVersion')
    BrickTag = apps.get_model('mapp', 'BrickTag')
    brick_version_model = BrickVersion.objects.get(version=bv)

    g = BrickGraph(load_brick=True)
    all_tags = list(g.g.subjects(RDF.type, BRICK['Tag']))
    for tag in all_tags:
        ns, t = tag.split("#")
        bt = BrickTag(tag=t, version=brick_version_model, namespace=ns)
        bt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_brick_version),
        migrations.RunPython(generate_haystack_version),
        migrations.RunPython(generate_brick_tags),
        migrations.RunPython(generate_haystack_marker_tags)
    ]
