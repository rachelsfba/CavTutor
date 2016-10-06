from django.core.urlresolvers import reverse

from django.contrib.auth.models import User as DjangoUser

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from . import views, models, serializers

# Create your tests here.

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
        self.assertEqual(models.Institution.objects.get(pk=2).name, data['name'])

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




""" A series of tests for the Tutee model and REST API. Follows CRUD model. """
class TuteeTestCase(APITestCase):

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
        self.new_test_course = models.Course.objects.create(
                institution=self.test_institution,
                name='Advanced Programming',
                abbr='CS 201',
                instructor = 'John Smith',
            )

        self.test_user2 = models.User.objects.create(
                f_name = 'daniel',
                l_name = 'saha',
                email = 'ds@localhost',
                username = 'dfasdsa',
                password = 'sdfasdfasdf',
            )

        self.test_user = models.User.objects.create(
                f_name = 'Andrea',
                l_name = 'Shaw',
                email = 'as@localhost',
                username = 'asdf',
                password = 'sadfasdf',
            )

        # a ddummy Tutor obj
        self.tutor_data = dict(
                user = self.test_user,
                course = self.test_course,
                adv_rate = '20.00',
            )
        self.test_tutor = models.Tutor.objects.create(**self.tutor_data)

        # a dummy Tutee object to test R, U, & D on
        self.tutee_data = dict(
                user = self.test_user,
                course = self.test_course,
                tutor = self.test_tutor,
            )
        self.test_tutee = models.Tutee.objects.create(**self.tutee_data)

        self.new_tutee_data = dict(
                user = self.test_user.pk,
                course = self.new_test_course.pk,
                tutor = self.test_tutor.pk,
            )
    def test_create(self):

        url = reverse('tutee-list')

        data = dict(
                user = self.test_user.pk,
                course = self.test_course.pk,
                tutor = self.test_tutor.pk,
            )

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.Tutee.objects.count(), 2)
        #self.assertEqual(models.Tutor.objects.get().user.pk, data['user'])

    def test_read_all(self):
        url = reverse('tutee-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('tutee-detail', args=[self.test_tutee.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse('tutee-detail', args=[self.test_tutee.id])

        response = self.client.put(url, self.new_tutee_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('tutee-detail', args=[self.test_tutee.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()








