# Create your tests here.
from django.test import TestCase
from generate import models
from os import path


class IndexViewTest(TestCase):

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
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['sites']), [])

    def test_upload(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "tests", "files", "carytown.json"))
        with open(filepath) as file:
            self.client.post('', {'upload': '', 'file': file})

        response = self.client.get('')
        sites = response.context['sites']
        self.assertEqual(len(sites), 2)


class CreateSiteTest(TestCase):

    def test_create(self):
        data = {
            'name': "Test Create Site",
            'city': "Golden",
            'state': "CO",
            'zip': 80401
        }
        response = self.client.post('/create_site/', data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('')
        self.assertEqual([site.name for site in response.context['sites']], ["Test Create Site"])


class CreateFromTemplateTest(TestCase):

    def test_upload_from_template(self):
        self.client.post('/create_from_template/', {'upload': 'resources/smalloffice.json'})
        response = self.client.get('')
        self.assertEqual([site.name for site in response.context['sites']],
                         ["s:-SmallOffice-ASHRAE 169-2013-5A created: 2020-05-04 20:29:25 -0600"])
