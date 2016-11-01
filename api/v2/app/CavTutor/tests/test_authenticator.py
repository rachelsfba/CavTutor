from django.core.urlresolvers import reverse
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password

import os
import hmac

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from CavTutor import views, models, serializers

""" 
   CavTutor.test_authenticator: A series of tests for the Authenticator model
   and REST API. Follows CRUD model. 
"""
class AuthenticatorTestCase(APITestCase):
    
    # Set up the class before each function call.
    def setUp(self):
        self.test_user = models.User.objects.create(
            f_name='Foo',
            l_name='Bar',
            email='foo.bar@somewhere.io',
            username='foo',
            password=make_password('bar'),
        )

        # a dummy Authenticator object to test R, U, & D on
        self.authenticator_data = dict(
            token=hmac.new(
                key=settings.SECRET_KEY.encode('utf-8'),
                msg=os.urandom(32),
                digestmod='sha256').hexdigest(),
            user=self.test_user,
            expiry_date=timezone.now() + timezone.timedelta(hours=8)
                )
        # Authenticator doesn't update
        # self.new_authenticator_data = dict(
        #     authenticator=hmac.new(
        #         key=settings.SECRET_KEY.encode('utf-8'),
        #         msg=os.urandom(32),
        #         digestmod='sha256').hexdigest()
        # )

        self.test_authenticator = models.Authenticator.objects.create(**self.authenticator_data)

    def test_create(self):

        url = reverse('authenticator-list')

        data = {
                'token': hmac.new(key=settings.SECRET_KEY.encode('utf-8'),
                            msg=os.urandom(32),
                            digestmod='sha256').hexdigest(),
                'user':  self.test_user.pk,
            }
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we create a second object in setUp()
        self.assertEqual(models.Authenticator.objects.count(), 2)

        #created_obj = models.User.objects.get(pk=2)
        #self.assertEqual(created_obj.username, data['username'])

    def test_read_all(self):
        url = reverse('authenticator-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_specific(self):
        url = reverse('authenticator-detail', args=[self.test_authenticator.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update(self):
    #     url = reverse('authenticator-detail', args=[self.test_authenticator.id])
    #
    #     response = self.client.put(url, self.new_authenticator_data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('authenticator-detail', args=[self.test_authenticator.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.client.logout()
