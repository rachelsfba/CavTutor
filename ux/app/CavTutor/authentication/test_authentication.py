#    from django.core.urlresolvers import reverse
#    from django.utils import timezone
#    
#    from rest_framework import status
#    from rest_framework.test import APIRequestFactory, APITestCase, APIClient
#    
#    """ 
#       CavTutor.authentication.test_authentication: A series of tests for the authentication backend.
#    """
#    class AuthenticationTestCase(APITestCase):
#    
#        def testBadLogin(self):
#            url = reverse('login')
#    
#            # tihs is not a valid user, so it should 404
#            postdata = { 
#                    'username': 'this is not a',
#                    'password': 'valid user',
#                }
#    
#            login_resp = self.client.post(url, data=postdata)
#    
#            self.assertEqual(login_resp.status_code, status.HTTP_404_NOT_FOUND)
#    
#    
#        def testGoodLogin(self):
#            url = reverse('login')
#    
#            # Jane is a user in the fixtures, so this goes through
#            postdata = { 
#                    'username': 'Jane',
#                    'password': 'jdoe123',
#                }
#    
#            login_resp = self.client.post(url, data=postdata)
#    
#            self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
