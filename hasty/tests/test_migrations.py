from django.test import TestCase
from django.db.models import Count
import pytest

from mapp.models import HaystackVersion, BrickVersion, HaystackMarkerTag, BrickTag, HaystackPointType
from brickschema.graph import Graph as BrickGraph
from brickschema.namespaces import BRICK
from rdflib import RDF


pytestmark = pytest.mark.django_db


class TestVersionData(TestCase):
    def test_brick_version(self):
        bv = BrickVersion.objects.filter(version='1.1')
        assert len(bv) == 1

        bv0 = bv[0]
        assert bv0.version == "1.1"

    def test_haystack_version(self):
        hv = HaystackVersion.objects.filter(version='3.9.9')
        assert len(hv) == 1
        hv0 = hv[0]
        assert hv0.version == "3.9.9"


class TestTags(TestCase):
    def test_haystack_marker_tags_exist(self):
        hv = HaystackVersion.objects.filter(version='3.9.9')
        assert len(hv) == 1
        hv = hv[0]
        should_exist = [

            # General
            "discharge",
            "air",
            "temp",
            "sensor",
            "point",
            "cmd",

            # 3.9.9
            "plantTertiaryLoop",
            "fuelOilHeating",
            "naturalGasHeating",
            "hvacZonePoints",
            "lightingZonePoints",
            "waterCooling",

            # 3.9.8
            "filter",
            "co",
            "diverting",
            "volume",
            "constantAirVolume",
            "variableAirVolume",
            "condenserOpenLoop",
            "condenserClosedLoop",
            "humidifier",
            "economizing",
            "dessicantDehumidifier",
            "pointGroup",

            # 3.9.7
            "freezeStat",
            "heatWheel",
            "faceBypass",
            "reheat",
            # "ductArea",  TODO: remove
            "perimeterHeat",
            "circ",
            "flue",

            # 3.9.6
            "dataCenter",
            "rack",
            "panel",

            # 3.9.4
            "motor",
            "vfd",
            "actuator",
            "unitVent",
            "movingWalkway",
            "heatExchanger",
            "coil",
            "heatingCoil",
            "coolingCoil",

            # 3.9.3
            "fan",
            "damper",
            "pump",
            "valve",
            "airTerminalUnit",
            "cav",
            "vav",
            "airHandlingEquip",
            "mau",
            "rtu",
            "fcu",
            # "uv",  deprecated 3.9.4
            "heatPump",
            "fumeHood",
            "radiantEquip",
            "radiator",
            "radiantFloor",
            "chilledBeam",
            "thermostat",
            "luminaire",
            "verticalTransport",
            "elevator",
            "escalator"
        ]

        for marker in should_exist:
            t = HaystackMarkerTag.objects.filter(tag=marker, version=hv)
            assert len(t) == 1, f"Marker tag {marker} should exist for Haystack version: {hv.version}"

        should_not_exist = [
            "phase",
            "stage",

            "oilHeating",
            "gasHeating",
            "uv"
        ]

        for marker in should_not_exist:
            t = HaystackMarkerTag.objects.filter(tag=marker, version=hv)
            assert len(t) == 0, f"Marker tag {marker} should NOT exist for Haystack version: {hv.version}, but does."

    def test_brick_tags(self):
        bv = '1.1'
        bvm = BrickVersion.objects.filter(version=bv)
        assert len(bvm) == 1
        bvm = bvm[0]

        g = BrickGraph(load_brick=True)
        all_tags = list(g.g.subjects(RDF.type, BRICK['Tag']))
        bt = BrickTag.objects.filter(version=bvm)
        assert len(all_tags) == len(bt), f"For Brick version {bvm.version}: {len(all_tags)} tags exist in the Brick ttl file.  Only {len(bt)} tags are populated in the database."


class TestHaystackPointTypes(TestCase):
    def test_good_point_types(self):
        hv = '3.9.9'
        hv = HaystackVersion.objects.filter(version=hv)
        assert len(hv) == 1
        hpt = HaystackPointType.objects.filter(version=hv[0])
        hpt_annotated = hpt.annotate(c=Count('marker_tags'))

        # damper cmd
        point_type = get_hpt_given_marker_tags(['damper', 'cmd', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone temp sp
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'temp', 'sensor', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # occupied sensor point
        point_type = get_hpt_given_marker_tags(['occupied', 'sensor', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone co2
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'co2', 'sensor', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone occ heating sp
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'temp', 'occ', 'heating', 'sp', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone occ cooling sp
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'temp', 'occ', 'cooling', 'sp', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone unocc heating sp
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'temp', 'unocc', 'heating', 'sp', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

        # zone unocc cooling sp
        point_type = get_hpt_given_marker_tags(['zone', 'air', 'temp', 'unocc', 'cooling', 'sp', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 1

    def test_bad_point_types(self):
        hv = '3.9.9'
        hv = HaystackVersion.objects.filter(version=hv)
        assert len(hv) == 1
        hpt = HaystackPointType.objects.filter(version=hv[0])
        hpt_annotated = hpt.annotate(c=Count('marker_tags'))

        point_type = get_hpt_given_marker_tags(['damper', 'cmd', 'point', 'sensor'], hv[0], hpt_annotated)
        assert len(point_type) == 0

        point_type = get_hpt_given_marker_tags(['discharge', 'air', 'temp', 'sensor', 'point'], hv[0], hpt_annotated)
        assert len(point_type) == 0


def get_hpt_given_marker_tags(marker_tags, hv_object, hpt_annotated):
    hmt = HaystackMarkerTag.objects.filter(version=hv_object)
    marker_tag_models = hmt.filter(tag__in=marker_tags)
    assert len(marker_tag_models) == len(marker_tags)

    temp = hpt_annotated.filter(c=len(marker_tag_models))
    for tag in marker_tag_models:
        temp = temp.filter(marker_tags=tag)
    return temp
