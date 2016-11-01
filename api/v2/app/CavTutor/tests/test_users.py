from django.core.urlresolvers import reverse

from django.contrib.auth.models import User as DjangoUser

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from CavTutor import views, models, serializers

""" A series of tests for the User model and REST API. Follows CRUD model. """
class UserTestCase(APITestCase):

    def setUp(self):
        # need to be a superuser to POST create requests
        self.superuser = DjangoUser.objects.create_superuser('root', 'root@localhost', 'secret')
        self.client.login(username='root', password='secret')

        # a dummy User object to test R, U, & D on
        self.data = dict(
                f_name = 'Andrea',
                l_name = 'Shaw',
                email = 'as@localhost',
                username = 'asdf',
                password = 'sadfasdf',
                )

        self.new_data = dict(
                f_name = 'asfdklsdajfklads',
                l_name = 'Shaw',
                email = 'as@localhost',
                username = 'asdf',
                password = 'sadfasdf',
                )

        self.test_user = models.User.objects.create(**self.data)

    def test_create(self):

        url = reverse('user-list')

        data = dict(
                f_name = 'ASFDSDFd',
                l_name = 'asfdhasdfaw',
                email = 'aasds@localhost',
                username = 'aasdfsdf',
                password = 'sadfaasdfsdf',
                )

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.User.objects.count(), 2)

        #created_obj = models.User.objects.get(pk=2)
        #self.assertEqual(created_obj.username, data['username'])

    def test_read_all(self):
        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('user-detail', args=[self.test_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('user-detail', args=[self.test_user.id])

        response = self.client.put(url, self.new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('user-detail', args=[self.test_user.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()
