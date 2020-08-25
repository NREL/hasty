from django.test import TestCase
from generate import models


class TestGetSites(TestCase):

    def setUp(self):
        test_site = models.Site.objects.create(
            name="Test Site",
            city="Golden",
            state="CO",
            zip=80401
        )
        models.AirHandler.objects.create(
            name="Test AHU",
            site_id=test_site,
            tagset="tags",
            brick_class="brick"
        )

    def test_sites(self):
        response = self.client.get('/api/sites')
        self.assertEqual(response.status_code, 200)
