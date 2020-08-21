# Create your tests here.
from django.test import TestCase
from . import models


class IndexViewTest(TestCase):

    def setUp(self):
        test_site = models.Site.objects.create(
            id=1111,
            name="Test Site",
            city="Golden",
            state="CO",
            zip=80401
        )
        models.AirHandler.objects.create(
            id=2222,
            name="Test AHU",
            site_id=test_site,
            tagset="tags",
            brick_class="brick"
        )

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sites' in response.context)
        self.assertTrue('ahus' in response.context)
        self.assertEqual([site.name for site in response.context['sites']], ["Test Site"])
        self.assertEqual([ahu.name for ahu in response.context['ahus']], ["Test AHU"])

    def test_delete(self):
        # Get the test_site for the UUID
        response = self.client.get('')
        site = response.context['sites'][0]
        # Send the delete in a POST
        response = self.client.post('', {'id': site.id, 'delete': ""})
        # The site GET request should now be 0
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['sites']), [])
