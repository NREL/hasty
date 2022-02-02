# Create your tests here.
from django.test import TestCase
from generate import models
from os import path


class IndexViewTest(TestCase):
    # Tests the ListSites view in views.py
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
        filepath = path.abspath(path.join(basepath, "..", "..", "tests", "files", "mediumOffice_haystack.json"))
        with open(filepath) as file:
            self.client.post('', {'upload': '', 'file': file})

        response = self.client.get('')
        sites = response.context['sites']
        self.assertEqual(len(sites), 2)


class CreateSiteTest(TestCase):
    # Tests the CreateSite view in views.py
    def test_create(self):
        data = {
            'name': "Test Create Site",
            'city': "Golden",
            'state': "CO",
            'zip': 80401
        }
        response = self.client.post('/create_site/', data)
        # 302 because of a redirect
        self.assertEqual(response.status_code, 302)

        response = self.client.get('')
        self.assertEqual([site.name for site in response.context['sites']], ["Test Create Site"])


class CreateFromTemplateTest(TestCase):
    # Tests the CreateFromTemplate view in views.py
    def test_upload_from_template(self):
        self.client.post('/create_from_template/', {'upload': 'resources/smalloffice.json'})
        response = self.client.get('')
        self.assertEqual([site.name for site in response.context['sites']],
                         ["s:-SmallOffice-ASHRAE 169-2013-5A created: 2020-05-04 20:29:25 -0600"])


class SiteDetailTest(TestCase):
    # Tests the SiteDetail view in views.py
    def test_detail_with_site_id(self):
        site = models.Site.objects.create(
            name="Test Site with ID",
            city="Golden",
            state="CO",
            zip=80401
        )
        models.AirHandler.objects.create(
            name="Test AHU with ID",
            site_id=site,
            tagset="tags",
            brick_class="brick"
        )
        response = self.client.get('/site/{}'.format(site.id))
        self.assertEqual(response.status_code, 200)
        added_site = response.context['site']
        self.assertEqual([added_site.name], ["Test Site with ID"])
        self.assertEqual([ahu.name for ahu in response.context['ahus']], ["Test AHU with ID"])
        # TODO: add terminal unit info and types

    def test_create_ahu(self):
        # Test create air_handler in site detail view
        site = models.Site.objects.create(
            name="Test Site with ID",
            city="Golden",
            state="CO",
            zip=80401
        )
        data = {
            'create_air_handler': "",
            'name': "Test create AHU with ID",
            'site_id': site,
            'pre_heat_coil': ['35'],
            'heating_coil_type': ['35'],
            'cooling_coil_type': ['44'],
            'heating_cooling_coil_type': ['41'],
            'supp_heat_coil': ['35'],
            'discharge_fan_type': ['4'],
            'return_fan_type': ['7'],
            'exhaust_fan_type': ['10'],
            'terminal_unit_default_type': ['1'],
            'num_terminal_units': ['2'],
            'discharge_air_temperature_reset_strategy': ['1'],
            'discharge_air_pressure_reset_strategy': ['1'],
            'economizer_control_strategy': ['1'],
            'ventilation_control_strategy': ['1']
        }
        response = self.client.post('/site/{}'.format(site.id), data)
        # redirects to the ahu view
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/site/{}'.format(site.id))
        self.assertEqual([ahu.name for ahu in response.context['ahus']], ["Test create AHU with ID"])


class AirHandlerTest(TestCase):

    def setUp(self):
        self.temp_site = models.Site.objects.create(
            name="Test Site with ID from site.ahu view",
            city="Golden",
            state="CO",
            zip=80401
        )
        self.temp_ahu = models.AirHandler.objects.create(
            name="Test AHU with ID from site.ahu view",
            site_id=self.temp_site,
            tagset="tags",
            brick_class="brick"
        )
        # confirm adding terminal units properly
        self.temp_terminal = models.TerminalUnit.objects.create(
            name="Test Terminal Unit with ID from site.ahu view",
            object_id=self.temp_ahu.id,
            tagset="tags",
            brick_class="brick"
        )

    def test_ahu_terminal_with_id(self):
        response = self.client.get('/site/{}/ahu/{}'.format(self.temp_site.id, self.temp_ahu.id))
        added_site = response.context['site']
        added_ahu = response.context['ahu']
        self.assertEqual([added_site.name], ["Test Site with ID from site.ahu view"])
        self.assertEqual([added_ahu.name], ["Test AHU with ID from site.ahu view"])

    def test_rename_terminal_unit(self):
        data = {
            "{}".format(self.temp_terminal.id): "New Name",
            'terminal_unit': 1,
            'update_terminal_unit': ""
        }
        response = self.client.post('/site/{}/ahu/{}'.format(self.temp_site.id, self.temp_ahu.id), data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/site/{}/ahu/{}'.format(self.temp_site.id, self.temp_ahu.id))
        self.assertTrue('terminal_units' in response.context)
