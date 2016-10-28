# views for the Uesr model
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from rest_framework import status

from core.settings import UX_BASE 
from .forms import *

import json

def listings(request):

    json_data = urlopen(UX_BASE + 'users/').read().decode('utf-8')
    context = {
            'users' : json.loads(json_data),
        }

    return render(request, 'CavTutor/user-list.html', context)

def detail(request, user_id):
    try:
        json_data = urlopen(UX_BASE + 'users/' + user_id).read().decode('utf-8')
        context = {'user' : json.loads(json_data) }

        return render(request, 'CavTutor/user-detail.html', context)
    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "user",
                "id": user_id,
            })

@csrf_protect
def login(request):

    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        login_form = UserLoginForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        login_form = UserLoginForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if login_form.is_valid():
            # Forms will sanitize for us
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # Redirect to index page after successful login.
            next_page = reverse('index')

            # Retrieve login response and associated status code
            ux_response, status_code = _user_login_ux(username, password)

            if not ux_response or not ux_response['token']:
                status = "incorrect"
            else:
                auth_cookie = ux_response['token']
                expiry = ux_response['expiry_date']

                www_response = HttpResponseRedirect(next_page)
                www_response.set_cookie("auth_token", auth_cookie, expires=expiry)

                return www_response
        else:
            status = "incomplete"

    return render(request, 'CavTutor/user-login.html', {
            'form': login_form,
            'status': status,
        })


def _user_login_ux(username, password):
    data = {
            'username': username,
            'password': password,
        }

    encoded_data = urlencode(data).encode('utf-8')
    try:
        request = urlopen(UX_BASE + 'users/login/', data=encoded_data)
    except HTTPError as e:
        return None, 404

    return json.loads(request.read().decode('utf-8')), request.getcode()

def register(request):
    return # yet to be implemented

def logout(request):
    return # yet to be implemented

# vim: ai ts=4 sts=4 et sw=4
