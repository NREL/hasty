import os

import brickschema
from mapp.resources.migration_utils import generate_ranked_inference_csv, generate_point_protos


def test_generate_ranked_inference_csv():
    """
    Test whether csv file is generated
    Test whether headers match expectations
    Test whether first row inference matches expectations
    """
    brick_version = '1.1'
    haystack_version = '3.9.9'
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
    if not os.path.isdir(p):
        os.makedirs(p)
    fp = f"{p}/ranked_mapping_Brick-{brick_version}_Haystack-{haystack_version}_py-brickschema-{brickschema.__version__}.csv"
    if os.path.isfile(fp):
        os.remove(fp)
    output = generate_ranked_inference_csv(out_file=fp, brick_version=brick_version, haystack_version=haystack_version)
    assert os.path.isfile(fp)
    assert isinstance(output, list)
    assert output[0] == ['Brick Version', brick_version]
    assert output[1] == ['Haystack Version', haystack_version]
    assert output[2] == ['Brick Inference Version', brickschema.__version__]
    assert output[5] == ['air-co2-point', 'Point', 'Point']


def test_generate_point_protos():
    haystack_version = '3.9.9'
    protos = generate_point_protos(haystack_version)
    assert isinstance(protos, list)
    assert len(protos) == 431

    count_non_marker_protos = 0
    count_protos_with_doublequote = 0
    for proto in protos:
        if ':' in proto:
            count_non_marker_protos += 1
        if '"' in proto:
            count_protos_with_doublequote += 1
    assert count_non_marker_protos == 33  # stage:1 and phase:A points
    assert count_protos_with_doublequote == 0
