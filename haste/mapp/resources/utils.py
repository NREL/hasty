import os
from uuid import uuid4
import json

from bs4 import BeautifulSoup
from brickschema.inference import HaystackInferenceSession


def create_initial_mapper(apps, schema_editor):
    Mapper = apps.get_model('mapp', 'Mapper')
    m = Mapper(brick_version='V1.1', haystack_version='V3.9.9')
    m.save()


def infer_points(apps, schema_editor, haystack_version='V3.9.9'):
    Mapper = apps.get_model('mapp', 'Mapper')
    PointMapping = apps.get_model('mapp', 'PointMapping')
    m = Mapper.objects.first()
    hi = HaystackInferenceSession("https://example.com/carytown")
    all_protos = read_all_protos(haystack_version)
    for proto in all_protos:
        try:
            a, b = hi.infer_entity(proto, str(uuid4()))
            bc = a[0][2].split("#")[1]
            pm = PointMapping(brick_class=bc, haystack_tagset=json.dumps(proto), parent_map=m)
            pm.save()
        except IndexError:
            pm = PointMapping(brick_class=None, haystack_tagset=json.dumps(proto), parent_map=m)
            pm.save()


def read_all_protos(haystack_version):
    print(os.getcwd())
    p = os.path.join(os.getcwd(), f"mapp/resources/haystack/{haystack_version}/index-pointProtos.html")
    with open(p, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, features="html.parser")
    all_protos = soup.find_all('th')

    # Generate a list of sets
    all_protos = [p.a.text for p in all_protos]
    all_protos = [p.split(' ') for p in all_protos]
    return(all_protos)
