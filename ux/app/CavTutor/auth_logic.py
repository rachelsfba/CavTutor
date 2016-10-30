import requests
import os
import hmac
import json
import datetime

import core.settings as settings

from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password
from urllib.request import urlopen
from urllib.error import HTTPError

from urllib.parse import urlencode

API_VERSION = 'v2'

API_BASE = 'http://api:8000/api/' + API_VERSION + "/"
UX_BASE = 'http://localhost:8000/'

HTTP_ERROR_500 = json.dumps(dict(detail="HTTP 500 Error: Internal Service Error"))

HTTP_ERROR_400 = json.dumps(dict(detail="HTTP 400 Error: Bad Request"))
HTTP_ERROR_404 = json.dumps(dict(detail="HTTP 404 Error: File Not Found"))

def logout(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        authenticators = json.loads(urlopen(API_BASE + 'authenticators/?format=json').read().decode('utf-8'))
    except HTTPError:
        return HttpResponseNotFound(HTTP_ERROR_404)

    response = {
            'ok': False,
            'message': 'Cookie with token {} was deleted before ' + 
                       'I could do it myself!'.format(authenticator['token']),
        }

    for authenticator in authenticators:
        if authenticator['token'] == request.POST.get('auth_token'):
            _delete_cookie(request, authenticator['id'])
            
            response['ok'] = True
            response['message'] = 'Successfully deleted cookie with token ' + authenticator['token']

            break

    return HttpResponse(json.dumps(response))

def login(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest(HTTP_ERROR_400)
   

    # attempt to get a list of all users from the API, so we can validate
    # against the username and password in the POST data
    user_list = requests.get(API_BASE + 'users/?format=json')

    if user_list.status_code != 200:
        # If users listing didn't work sfor some reason, 
        return HttpResponseNotFound(HTTP_ERROR_404)
    
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
                return HttpResponseServerError(HTTP_ERROR_500)
            
            #return cookie to front end
            return HttpResponse(api_auth_data)

    return HttpResponseNotFound(HTTP_ERROR_404)

def register(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest(HTTP_ERROR_400)
   
    # attempt to get a list of all users from the API, so we can see if the user already exists in our system
    user_list = requests.get(API_BASE + 'users/?format=json')

    if user_list.status_code != 200:
        # If users listing didn't work sfor some reason, 
        return HttpResponseServerError(HTTP_ERROR_500)
    
    # we have to iterate over all the users in the entire listing. need to find
    # a more RESTful and efficient way
    for user in user_list.json():
        # for every user in the data, check if their username or email
        # match what is in the POST data
        if request.POST.get('username') == user['username'] or \
            request.POST.get('email') == user['email']:
            
            # user already exists in system
            return HttpResponseBadRequest(HTTP_ERROR_400)
    
    register_req = requests.post(API_BASE + 'users/', data=request.POST)

    return HttpResponse(register_req.text, status=201)

def validate_user_cookie(request):
    
    auth_cookie = request.POST.get("token")
    
    # check if the cookie was set
    if auth_cookie:
        # check if the cookie has expired
        json_data = requests.request('GET', API_BASE + 'authenticators/?format=json').text

        for authenticator in json.loads(json_data):
            if authenticator['token'] == auth_cookie:
                user_info = {
                            'user_id': authenticator['user']
                        }

                return HttpResponse(json.dumps(user_info))
        return HttpResponseNotFound(HTTP_ERROR_404)
    return HttpResponseBadRequest(HTTP_ERROR_400)

def _make_new_auth_cookie():

    authenticator = hmac.new(
            key = settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256').hexdigest()

    return authenticator

def _delete_cookie(request, auth_id):
    del_cookie = requests.request('DELETE', API_BASE + 'authenticators/{}/'.format(auth_id))

    return del_cookie

