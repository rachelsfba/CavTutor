from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

import requests
import json

from core.settings import UX_BASE 


def login_required(func):
    def wrap(request, *args, **kwargs):
        # try authenticating the user
        user = _get_loggedin_user(request)

        # failed
        if not user:
            # redirect the user to the login page
            return HttpResponseRedirect(reverse('user-login'))
        return func(request, *args, **kwargs)

    return wrap

def nologin_required(func):
    def wrap(request, *args, **kwargs):
        # try authenticating the user
        user = _get_loggedin_user(request)
        
        # failed -- good!
        if not user:
            return func(request, *args, **kwargs)
        # user was actually authenticated, so let's just send them to the home page for now
        return HttpResponseRedirect(reverse('index'))

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
