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

import requests
API_VERSION = 'v2'

API_BASE = 'http://api:8000/api/' + API_VERSION + "/"
UX_BASE = 'http://localhost:8000/'

HTTP_ERROR_500 = json.dumps(dict(detail="HTTP 500 Error: Intersal Service Error"))

HTTP_ERROR_400 = json.dumps(dict(detail="HTTP 400 Error: Bad Request"))
HTTP_ERROR_404 = json.dumps(dict(detail="HTTP 404 Error: File Not Found"))

def institution_new(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    # attempt to get a list of all users from the API, so we can see if the user already exists in our system
    inst_list = requests.get(API_BASE + 'institutions/?format=json')

    if inst_list.status_code != 200:
        # If users listing didn't work sfor some reason, 
        return HttpResponseServerError(HTTP_ERROR_500)
    
    # we have to iterate over all the users in the entire listing. need to find
    # a more RESTful and efficient way
    for inst in inst_list.json():
        # for every user in the data, check if their username or email
        # match what is in the POST data
        if request.POST.get('name') == inst['name']:
            # user already exists in system
            return HttpResponseBadRequest(HTTP_ERROR_400)
    


    new_inst_data = requests.post(API_BASE + 'institutions/', data=request.POST)

    if new_inst_data.status_code != 201:
        return HttpResponseServerError(HTTP_ERROR_500)
    return HttpResponse(new_inst_data.text, status=201)


