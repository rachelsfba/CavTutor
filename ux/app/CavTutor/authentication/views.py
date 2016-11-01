"""
    MODULE:
    CavTutor.authentication.views
    
    DESCRIPTION:
    Handles authentication server-side logic, such as logging in, logging out,
    creating cookies, and user registration.
"""

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """
import requests, json 

""" These libraries are needed for cookie token generation. """
import os, hmac

""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE

"""  We utilize some common Django idioms, so fetch those implementations. """
from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status

"""
Handles logout requests by deleting the user's authentication cookie.

@param request a django.http.HttpRequest object
@return a response of type django.http.HttpResponse (or related subclass) with
    the proper HTTP status code and any related data
"""
def logout(request):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    authenticators = requests.get(API_BASE + 'authenticators')

    if authenticators.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    response = {
            'ok': False,
            'message': 'Cookie with token {} was deleted before ' + 
                       'I could do it myself!'.format(authenticator['token']),
        }

    for authenticator in authenticators.json():
        if authenticator['token'] == request.POST.get('auth_token'):
            _delete_cookie(request, authenticator['id'])
            
            response['ok'] = True
            response['message'] = 'Successfully deleted cookie with token ' + authenticator['token']

            break

    return HttpResponse(json.dumps(response))

"""
Handles login requests by validating username and password combination
against the database. 

@param request a django.http.HttpRequest object
@return a response of type django.http.HttpResponse (or related subclass) with
    the proper HTTP status code and any related data
"""
def login(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest()
   

    # attempt to get a list of all users from the API, so we can validate
    # against the username and password in the POST data
    user_list = requests.get(API_BASE + 'users/?format=json')

    if user_list.status_code != 200:
        # If users listing didn't work sfor some reason, 
        return HttpResponseNotFound()
    
    # we have to iterate over all the users in the entire listing. need to find
    # a more RESTful and efficient way
    for user in user_list.json():
        # for every user in the data, check if their usernamd and password
        # match what is in the POST data
        if request.POST['username'] == user['username'] and \
            check_password(request.POST['password'], user['password']):
           
            # create a dictionary with the two fields the API will need to
            # create a new cookie
            response_context = {
                    'user': user['id'],
                    'token': _make_new_auth_cookie(),
                   }

            # try to post encoded_data to Authenticator api
            api_auth_data = requests.post(API_BASE + 'authenticators/', data=response_context)

            if api_auth_data.status_code != 201:
                return HttpResponseServerError()
            
            #return cookie to front end
            return HttpResponse(api_auth_data.text)

    return HttpResponseNotFound()

"""
Handles user registration by first checking if a user exists with that
information, then posting a creation request to the API.

@param request a django.http.HttpRequest object
@return a response of type django.http.HttpResponse (or related subclass) with
    the proper HTTP status code and any related data
"""
def register(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest()
   
    # attempt to get a list of all users from the API, so we can see if the user already exists in our system
    user_list = requests.get(API_BASE + 'users/?format=json')

    if user_list.status_code != 200:
        # If users listing didn't work sfor some reason, 
        return HttpResponseServerError()
    
    # we have to iterate over all the users in the entire listing. need to find
    # a more RESTful and efficient way
    for user in user_list.json():
        # for every user in the data, check if their username or email
        # match what is in the POST data
        if request.POST.get('username') == user['username'] or \
            request.POST.get('email') == user['email']:
            
            # user already exists in system
            return HttpResponseBadRequest()
    
    register_req = requests.post(API_BASE + 'users/', data=request.POST)

    return HttpResponse(register_req.text, status=201)

"""
Validates the authentication cookie token provided in the request parameter.

@param request a django.http.HttpRequest object
@return a response of type django.http.HttpResponse (or related subclass) with
    the proper HTTP status code and any related data
"""
def validate_user_cookie(request):
    
    auth_cookie = request.POST.get("token")
    
    # check if the cookie was set
    if auth_cookie:
        # check if the cookie has expired
        json_data = requests.get(API_BASE + 'authenticators/?format=json').json()

        for authenticator in json_data:
            if authenticator['token'] == auth_cookie:
                user_info = {
                            'user_id': authenticator['user']
                        }

                return HttpResponse(json.dumps(user_info))
        return HttpResponseNotFound()
    return HttpResponseBadRequest()

"""
Internal method that creates a new authenticator token.

@return an authenticator token
"""
def _make_new_auth_cookie():

    authenticator = hmac.new(
            key = settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256').hexdigest()

    return authenticator

"""
Internal method that sends a DELETE request to the API for the specified token.

@param request a django.http.HttpRequest object
@param auth_id the id of the authenticator token to delete
@return a requests object containing the response to the deletion request
"""
def _delete_cookie(request, auth_id):
    return requests.delete(API_BASE + 'authenticators/{}/'.format(auth_id))

