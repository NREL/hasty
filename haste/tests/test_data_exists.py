from django.test import TestCase
import pytest

from mapp.models import HaystackVersion, BrickVersion


@pytest.mark.django_db(transaction=True)
class TestVersionData(TestCase):
    def test_brick_version(self):
        bv = BrickVersion.objects.all()
        assert len(bv) == 1

        bv0 = bv[0]
        assert bv0.version == "1.1"

    def test_haystack_version(self):
        hv = HaystackVersion.objects.all()
        assert len(hv) == 1
        hv0 = hv[0]
        assert hv0.version == "3.9.9"
