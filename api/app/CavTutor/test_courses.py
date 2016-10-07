from django.core.urlresolvers import reverse

from django.contrib.auth.models import User as DjangoUser

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from . import views, models, serializers

""" A series of tests for the Course model and REST API. Follows CRUD model. """
class CourseTestCase(APITestCase):

    def setUp(self):
        # need to be a superuser to POST create requests
        self.superuser = DjangoUser.objects.create_superuser('root', 'root@localhost', 'secret')
        self.client.login(username='root', password='secret')

        self.test_institution = models.Institution.objects.create(name='Virginia Tech',
            abbr='VT',
            address='Blacksburg, VA')

        # a dummy Institution object to test R, U, & D on
        self.test_course = models.Course.objects.create(institution = self.test_institution,
                                                            name='Intro to CS',
                                                            abbr='cs 101',
                                                            instructor='dahadza')

    def test_create(self):

        url = reverse('course-list')

        data = dict(
                institution=self.test_institution.pk,
                name='Intro to Programming',
                abbr='CS 101',
                instructor = 'John Smith',
            )

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.Course.objects.count(), 2)
        self.assertEqual(models.Course.objects.get(pk=2).name, data['name'])

    def test_read_all(self):
        url = reverse('course-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('course-detail', args=[self.test_course.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('course-detail', args=[self.test_course.id])

        dummy_context = dict(request=APIRequestFactory().get('/'))

        data = dict(
                institution=self.test_institution.pk,
                name='Intro to Programming',
                abbr='CS 101',
                instructor = 'John Smith',
        )
        data.update({'name' : 'Intro to programming: section 2'})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('course-detail', args=[self.test_course.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()


