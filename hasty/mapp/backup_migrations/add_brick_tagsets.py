
from django.db import migrations

from brickschema.inference import BrickInferenceSession


def generate_brick_point_classes(apps, schema_editor):
    bv = '1.1'
    BrickPointType = apps.get_model('mapp', 'BrickPointType')
    BrickTag = apps.get_model('mapp', 'BrickTag')
    bis = BrickInferenceSession(load_brick=True)
    lup = bis._tag_sess.lookup
    pq = "SELECT ?p WHERE { ?p rdfs:subClassOf* brick:Point}"
    brick_points = bis.g.query(pq)
    for p in brick_points:
        pt = p[0].split("#")[1]
        brick_point = BrickPointType(brick_class=pt)
        brick_point.save()
        for k, v in lup.items():
            if len(v) > 0:
                if pt == list(v)[0]:
                    tags = list(k)
                    for t in tags:
                        bt = BrickTag.objects.filter(
                            tag=t, version__version=bv)
                        if len(bt) == 1:
                            brick_point.tags.add(bt[0])
                        else:
                            print(f"Brick tag: {t} was not found.")


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0004_auto_20200731_0309'),
    ]

    operations = [
        migrations.RunPython(generate_brick_point_classes)
    ]
