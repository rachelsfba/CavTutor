from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

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

def _validate_user_cookie(request):
    auth_cookie = request.COOKIES.get("auth_cookie")

    # check if the cookie was set
    if auth_cookie:
        # check if the cookie has expired
        json_data = urlopen(UX_BASE + 'authenticators/').read().decode('utf-8')

        for authenticator in json.loads(json_data):
            if authenticator['token'] == auth_cookie:
                return True

    return False

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
