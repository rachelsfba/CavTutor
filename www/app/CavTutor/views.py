from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import requests

from rest_framework import status

from core.settings import UX_BASE 

import json

def login_required(func):
    def wrap(request, *args, **kwargs):
        # try authenticating the user
        user = _validate_user_cookie(request)

        # failed
        if not user:
            # redirect the user to the login page
            return HttpResponseRedirect(reverse('login'))
        else:
            return func(request, *args, **kwargs)

    return wrap

def _validate_user_cookie(auth_cookie):

    # check if the cookie was set
    if auth_cookie:
        # check if the cookie has expired
        postdata = {"token": auth_cookie}

        validate_req = requests.post(UX_BASE + 'validate/', data=postdata)

        if validate_req.status_code == 200:
            return validate_req.json()['user_id']

    return None

def _get_loggedin_user(request):
    auth_cookie = request.COOKIES.get("auth_token")
    
    user_id = str(_validate_user_cookie(auth_cookie))
    
    if user_id:
        user_data = requests.get(UX_BASE + 'users/' + user_id)

        if user_data.status_code == 200:
            return user_data.json()
    return 
"""
    Index page
"""
def index(request):

    context = {
            "title" : "CavTutor: A Tutoring Marketplace",
            "models" : ['institutions', 'users', 'courses', 'tutors', 'tutees'],
        }

    return render(request, 'CavTutor/index.html', context)


    json_data = urlopen(UX_BASE + 'institutions/').read().decode('utf-8')

# vim: ai ts=4 sts=4 et sw=4
