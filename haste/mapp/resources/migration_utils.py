import os
from uuid import uuid4
import csv

from bs4 import BeautifulSoup
import brickschema
from brickschema.inference import HaystackInferenceSession

from mapp.models import BrickVersion, HaystackVersion, InferenceVersion, BrickPointType, HaystackPointType, PointTypeMap


# def create_initial_mapper(apps, schema_editor, brick_version='V1.1', haystack_version='V3.9.9'):
#     """
#     create a Mapper class with defined versions of Brick and Haystack.  The version of they py-brickschema
#     package is dependent on the current package installed.
#     :param apps:
#     :param schema_editor:
#     :return:
#     """
#     Mapper = apps.get_model('mapp', 'Mapper')
#     m = Mapper.objects.filter(brick_version=brick_version, haystack_version=haystack_version, brick_inference_version=brickschema.__version__)
#     assert len(m) == 0, f"Mapper with versions already exists: brick_version: {brick_version}, haystack_version: {haystack_version}, " \
#                         f"brick_inference_version: {brickschema.__version__}.  Either remove this Mapper instance from the database " \
#                         f"or try switching to a different version of brickschema and re-running the migration."
#     m = Mapper(brick_version=brick_version, haystack_version=haystack_version, brick_inference_version=brickschema.__version__)
#     m.save()
#
#
# def infer_points(apps, schema_editor, brick_version='V1.1', haystack_version='V3.9.9'):
#     """
#     Given versions of Brick, Haystack, (and using the version of py-brickschema installed), this
#     function will utilize the py-brickschema package to inference the Brick point type given a
#     list of Haystack tags.  Tagsets for the Haystack version of interest must be available -
#     :param apps:
#     :param schema_editor:
#     :param brick_version:
#     :param haystack_version:
#     :return:
#     """
#     Mapper = apps.get_model('mapp', 'Mapper')
#     PointMapping = apps.get_model('mapp', 'PointMapping')
#     m = Mapper.objects.get(haystack_version=haystack_version, brick_version=brick_version, brick_inference_version=brickschema.__version__)
#     hi = HaystackInferenceSession("https://example.com/carytown")
#     all_protos = generate_point_protos(haystack_version)
#     for proto in all_protos:
#         try:
#             a, b = hi.infer_entity(proto, str(uuid4()))
#             bc = a[0][2].split("#")[1]
#             pm = PointMapping(brick_class=bc, haystack_tagset=json.dumps(proto), parent_map=m)
#             pm.save()
#         except IndexError:
#             pm = PointMapping(brick_class=None, haystack_tagset=json.dumps(proto), parent_map=m)
#             pm.save()


def generate_point_protos(haystack_version, markers_only=False):
    """
    Generate all point protos for a given Haystack version.  This function parses the
    'index-pointProtos.html' file in order to generate the tagsets.
    :param haystack_version: <str> version of Haystack, i.e. 'V3.9.9'
    :return: list, each element in the list is a string with a tagset, as 'tag1-tag2'.
    """
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"haystack/{haystack_version}/index-pointProtos.html")
    with open(p, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, features="html.parser")
    all_protos = soup.find_all('th')

    # Generate a list of sets
    all_protos = [p.a.text.replace(' ', '-') for p in all_protos]
    all_protos = [p.replace('"', '') for p in all_protos]
    if markers_only:
        all_protos = [proto for proto in all_protos if ':' not in proto]
    return all_protos


def generate_ranked_inference_csv(out_file, brick_version='1.1', haystack_version='3.9.9'):
    """
    generate a CSV file for a given brick, haystack, and py-brickschema version.  The CSV file
    contains a Haystack tagset in the first column, followed by a series of ranked Brick inference
    types.
    :param out_file:
    :param brick_version:
    :param haystack_version:
    :return: list, list of lists
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
    for proto in all_protos:
        temp = [proto]
        try:
            triple, ranked_inferences = hi.infer_entity(proto.split("-"), str(uuid4()))
            temp += [i[2][0] for i in ranked_inferences]
        except IndexError:
            temp += [None]

        output.append(temp)

    with open(out_file, 'w+') as f:
        wr = csv.writer(f)
        wr.writerows(output)

    return output


def verify_single_versions(brick_version, haystack_version, inference_version):
    bv = BrickVersion.objects.filter(version=brick_version)
    assert len(bv) == 1
    bv = bv[0]

    hv = HaystackVersion.objects.filter(version=haystack_version)
    assert len(hv) == 1
    hv = hv[0]

    iv = InferenceVersion.objects.filter(version=inference_version)
    assert len(iv) == 1
    iv = iv[0]

    return (bv, hv, iv)


def generate_point_type_map(brick_version, haystack_version, inference_version):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fp = f"{p}/ranked_mapping_Brick-{brick_version}_Haystack-{haystack_version}_py-brickschema-{inference_version}.csv"

    map = []
    with open(fp, 'r') as f:
        reader = csv.reader(f)
        for i in range(5):
            next(reader)
        for r in reader:
            if ':' not in r[0]:
                map.append([r[0], r[1]])
    return map


def add_map_to_db(map, brick_version, haystack_version, inference_version):
    bv, hv, iv = verify_single_versions(brick_version, haystack_version, inference_version)
    for row in map:
        hp = HaystackPointType.objects.filter(haystack_tagset=row[0], version=hv)
        bp = BrickPointType.objects.filter(brick_class=row[1], version=bv)
        ptm = False
        if len(hp) == 1 and len(bp) == 1:
            hp = hp[0]
            bp = bp[0]
            ptm = PointTypeMap(inference_version=iv, haystack_version=hv, brick_version=bv, brick_point=bp, haystack_point=hp)
        elif len(hp) == 1 and len(bp) == 0:
            hp = hp[0]
            ptm = PointTypeMap(inference_version=iv, haystack_version=hv, brick_version=bv, haystack_point=hp)
            print(f"PointTypeMap for HaystackPointType: {hp.marker_tags}; Inference Version: {iv.version}, Brick Version: {bv.version} did not have a BrickPointType")
        elif len(hp) == 0 and len(bp) == 1:
            bp = bp[0]
            ptm = PointTypeMap(inference_version=iv, haystack_version=hv, brick_version=bv, brick_point=bp)
            print(f"PointTypeMap for BrickPointType: {bp.brick_class}; Inference Version: {iv.version}, Brick Version: {bv.version} did not have a HaystackPointType")

        if ptm:
            ptm.save()
        else:
            print(f"PointTypeMap for: {row[0]}, {row[1]} was not created.")
