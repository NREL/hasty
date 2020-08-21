from django.test import TestCase
import pytest

from mapp.models import HaystackVersion, BrickVersion, HaystackMarkerTag, BrickTag
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
