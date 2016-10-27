from django.core.urlresolvers import reverse

from django.contrib.auth.models import User as DjangoUser

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from . import views, models, serializers

""" A series of tests for the Tutor model and REST API. Follows CRUD model. """
class TutorTestCase(APITestCase):

    def setUp(self):
        # need to be a superuser to POST create requests
        self.superuser = DjangoUser.objects.create_superuser('root', 'root@localhost', 'secret')
        self.client.login(username='root', password='secret')

        self.test_institution = models.Institution.objects.create(
                name='Virginia Tech',
                abbr='VT',
                address='Blacksburg, VA'
            )

        self.test_course = models.Course.objects.create(
                institution=self.test_institution,
                name='Intro to Programming',
                abbr='CS 101',
                instructor = 'John Smith',
            )

        self.test_user = models.User.objects.create(
                f_name = 'Andrea',
                l_name = 'Shaw',
                email = 'as@localhost',
                username = 'asdf',
                password = 'sadfasdf',
            )


        # a dummy Tutor object to test R, U, & D on
        self.data = dict(
                user = self.test_user,
                course = self.test_course,
                adv_rate = '20.00',
            )

        self.new_data = dict(
                user = self.test_user.pk,
                course = self.test_course.pk,
                adv_rate = '25.00',
            )

        self.test_tutor = models.Tutor.objects.create(**self.data)

    def test_create(self):

        url = reverse('tutor-list')

        data = dict(
                user = self.test_user.pk,
                course = self.test_course.pk,
                adv_rate = '15.00',
            )

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.Tutor.objects.count(), 2)
        #self.assertEqual(models.Tutor.objects.get().user.pk, data['user'])

    def test_read_all(self):
        url = reverse('tutor-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('tutor-detail', args=[self.test_tutor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('tutor-detail', args=[self.test_tutor.id])

        response = self.client.put(url, self.new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('tutor-detail', args=[self.test_tutor.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()
