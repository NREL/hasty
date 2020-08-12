import os

import brickschema
from mapp.resources.utils import generate_ranked_inference_csv


def test_generate_ranked_inference_csv(brick_version='1.1', haystack_version='3.9.9'):
    p = 'tests/outputs/'
    if not os.path.isdir(p):
        os.makedirs(p)
    fp = f"{p}/ranked_mapping_B{brick_version}_PH{haystack_version}_INFR{brickschema.__version__}.csv"
    if os.path.isfile(fp):
        os.remove(fp)
    generate_ranked_inference_csv(out_file=fp)
    assert os.path.isfile(fp)
