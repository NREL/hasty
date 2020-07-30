import os
from uuid import uuid4
import json
import csv

from bs4 import BeautifulSoup
import brickschema
from brickschema.inference import HaystackInferenceSession


def create_initial_mapper(apps, schema_editor, brick_version='V1.1', haystack_version='V3.9.9'):
    """
    create a Mapper class with defined versions of Brick and Haystack.  The version of they py-brickschema
    package is dependent on the current package installed.
    :param apps:
    :param schema_editor:
    :return:
    """
    Mapper = apps.get_model('mapp', 'Mapper')
    m = Mapper.objects.filter(brick_version=brick_version, haystack_version=haystack_version, brick_inference_version=brickschema.__version__)
    assert len(m) == 0, f"Mapper with versions already exists: brick_version: {brick_version}, haystack_version: {haystack_version}, " \
                        f"brick_inference_version: {brickschema.__version__}.  Either remove this Mapper instance from the database " \
                        f"or try switching to a different version of brickschema and re-running the migration."
    m = Mapper(brick_version=brick_version, haystack_version=haystack_version, brick_inference_version=brickschema.__version__)
    m.save()


def infer_points(apps, schema_editor, brick_version='V1.1', haystack_version='V3.9.9'):
    """
    Given versions of Brick, Haystack, (and using the version of py-brickschema installed), this
    function will utilize the py-brickschema package to inference the Brick point type given a
    list of Haystack tags.  Tagsets for the Haystack version of interest must be available -
    :param apps:
    :param schema_editor:
    :param brick_version:
    :param haystack_version:
    :return:
    """
    Mapper = apps.get_model('mapp', 'Mapper')
    PointMapping = apps.get_model('mapp', 'PointMapping')
    m = Mapper.objects.get(haystack_version=haystack_version, brick_version=brick_version, brick_inference_version=brickschema.__version__)
    hi = HaystackInferenceSession("https://example.com/carytown")
    all_protos = generate_point_protos(haystack_version)
    for proto in all_protos:
        try:
            a, b = hi.infer_entity(proto, str(uuid4()))
            bc = a[0][2].split("#")[1]
            pm = PointMapping(brick_class=bc, haystack_tagset=json.dumps(proto), parent_map=m)
            pm.save()
        except IndexError:
            pm = PointMapping(brick_class=None, haystack_tagset=json.dumps(proto), parent_map=m)
            pm.save()


def generate_point_protos(haystack_version):
    """
    Generate all point protos for a given Haystack version.  This function parses the
    'index-pointProtos.html' file in order to generate the tagsets.  The file structure for
    storing new versions of Haystack can be seen in the path below'
    :param haystack_version: <str> version of Haystack, i.e. 'V3.9.9'
    :return: List[List[],] list of lists, with tagsets
    """
    print(os.getcwd())
    p = os.path.join(os.getcwd(), f"mapp/resources/haystack/{haystack_version}/index-pointProtos.html")
    with open(p, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, features="html.parser")
    all_protos = soup.find_all('th')

    # Generate a list of sets
    all_protos = [p.a.text for p in all_protos]
    all_protos = [p.split(' ') for p in all_protos]
    return all_protos


def generate_ranked_inference_csv(out_file, brick_version='V1.1', haystack_version='V3.9.9'):
    """
    generate a CSV file for a given brick, haystack, and py-brickschema version.  The CSV file
    contains a Haystack tagset in the first column, followed by a series of ranked Brick inference
    types.
    :param out_file:
    :param brick_version:
    :param haystack_version:
    :return:
    """
    all_protos = generate_point_protos(haystack_version)
    output = [
        ['Brick Version', brick_version],
        ['Haystack Version', haystack_version],
        ['Brick Inference Version', brickschema.__version__],
        [],
        ['Haystack Proto', 'Brick Ranked Inference Types']
    ]

    hi = HaystackInferenceSession("https://example.bldg/#")
    # a, b = hi.infer_entity(all_protos[0], str(uuid4()))
    # print(a)
    # print([bs[2] for bs in b])
    for proto in all_protos:
        temp = [' '.join(proto)]
        try:
            triple, ranked_inferences = hi.infer_entity(proto, str(uuid4()))
            temp += [i[2][0] for i in ranked_inferences]
        except IndexError as ie:
            temp += [None]
            print(ie)

        output.append(temp)

    with open(out_file, 'w+') as f:
        wr = csv.writer(f)
        wr.writerows(output)
