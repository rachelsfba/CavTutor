from django.core.urlresolvers import reverse

from django.contrib.auth.models import User as DjangoUser

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from . import views, models, serializers

""" A series of tests for the Institution model and REST API. Follows CRUD model. """
class InstitutionTestCase(APITestCase):

    def setUp(self):
        # need to be a superuser to POST create requests
        self.superuser = DjangoUser.objects.create_superuser('root', 'root@localhost', 'secret')
        self.client.login(username='root', password='secret')

        # a dummy Institution object to test R, U, & D on
        self.test_institution = models.Institution.objects.create(name='Virginia Tech', abbr='VT', address='Blacksburg, VA')

    def test_create(self):

        url = reverse('institution-list')

        data = {
                'name' : 'University of Cascadia',
                'abbr' : 'UVA',
                'address' : '123 S Dr',
                }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.Institution.objects.count(), 2)
#        self.assertEqual(models.Institution.objects.get(pk=2).name, data['name'])

    def test_read_all(self):
        url = reverse('institution-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('institution-detail', args=[self.test_institution.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('institution-detail', args=[self.test_institution.id])

        dummy_context = dict(request=APIRequestFactory().get('/'))

        data = dict(name='Virginia Tech', abbr='VT', address='Blacksburg, VA')
        data.update({'name' : 'Virginia Polytechnic Institute and State University'})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('institution-detail', args=[self.test_institution.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()
