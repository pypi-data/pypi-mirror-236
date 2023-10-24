from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django.test import TestCase, RequestFactory, Client, override_settings


class ComponentTagTestCase(SilicaTestCase):
    def test_short_tag_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-tag-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component called with short name!")


    def test_components_in_subfolders_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-subfolder-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component in subfolder!")
