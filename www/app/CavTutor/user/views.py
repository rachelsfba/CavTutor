# views for the Uesr model
#from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from CavTutor.decorators import login_required, nologin_required
import requests

from rest_framework import status

from core.settings import UX_BASE 
from .forms import *

import json

def listings(request):

    json_data = requests.get(UX_BASE + 'users/').json()

    context = {
            'users' : json_data,
        }

    return render(request, 'CavTutor/user-list.html', context)

def detail(request, user_id):
    
    user_data = requests.get(UX_BASE + 'users/' + user_id)
    
    if user_data.status_code == 200:
        context = {'user' : user_data.json() }

        return render(request, 'CavTutor/user-detail.html', context)

    return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
            "model": "user",
            "id": user_id,
        })

@nologin_required
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

            # Retrieve login response 
            ux_response = _user_login_ux(username, password)

            if not ux_response or not ux_response['token']:
                status = "incorrect"
            else:
                auth_cookie = ux_response['token']
                expiry = ux_response['expiry_date']

                www_response = HttpResponseRedirect(next_page)
                #www_response = HttpResponse("Token: {} <br \><br \> Expiry Date: {}".format(auth_cookie, expiry))
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

    request = requests.post(UX_BASE + 'login/', data=data)

    if request.status_code == 200:
        return request.json()
    return 

@nologin_required
def register(request):

    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        register_form = UserRegisterForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        register_form = UserRegisterForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if register_form.is_valid():
            # Redirect to index page after successful login.
            next_page = reverse('index')

            # Retrieve login response 
            ux_register_response = _user_register_ux(request.POST)

            if not ux_register_response:
                # ux layer said the form was invalid;
                # probably means a user already exists with that username or email
                status = "invalid" 
            else:
                return render(request, 'CavTutor/user-register-after.html', {
                        'username': request.POST.get('username'),
                    })
        else:
            status = "incomplete"

    return render(request, 'CavTutor/user-register.html', {
            'form': register_form,
            'status': status,
        })


def _user_register_ux(postdata):
    request = requests.post(UX_BASE + 'register/', data=postdata)

    if request.status_code == 201: # HTTP_201_CREATED
        return request.json()
    return

@login_required
def logout(request):
    
    # Get the auth_token cookie, if it exists.
    auth_cookie = request.COOKIES.get('auth_token')

    # Forward user to index page.
    next_page = reverse('index')
    www_response = HttpResponseRedirect(next_page)

    # Did the auth_cookie actually exist?
    if auth_cookie:
        # If so, log them out in the database and delete their cookie.
        ux_response = _user_logout_ux(auth_cookie)
        www_response.delete_cookie('auth_token')
    
    return www_response

def _user_logout_ux(auth_cookie):
    
    data = {
            'auth_token': auth_cookie,
        }

    logout_response = requests.post(UX_BASE + 'logout/', data=data)

    if logout_response.status_code == 200:
        return logout_response.json()
    
    # If the error is just that the object didn't exist, oh well, no big
    # deal. We do the same thing if it existed or not.
    return None


