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

def search_listings(request):

    json_data = requests.get(UX_BASE + 'users/').json()

    context = {
            'users' : json_data,
        }

    return render(request, 'CavTutor/user-list.html', context)



def search(request):
    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        search_form = SearchForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        search_form = SearchForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if search_form.is_valid():
            # Forms will sanitize for us

            # Redirect to index page after successful login.
            #next_page = reverse('index')
            # next_page = request.POST.get('next','index')
            results = {"daniel":4, "richard":2, "matthew":1}
            
            # # Retrieve login response 
            ux_response = requests.post(UX_BASE + 'tutors/search/', data=search_form.cleaned_data)

            print(ux_response.json())


            return render(request, 'CavTutor/search.html', {
                 'results' : results,
                'form': search_form,
                'status': status})

            # if not ux_response or not ux_response['token']:
            #     status = "incorrect"
            # else:
            #     auth_cookie = ux_response['token']
            #     expiry = ux_response['expiry_date']

            #     context = {}
            #     www_response = HttpResponseRedirect(next_page)
            #     #www_response = HttpResponse("Token: {} <br \><br \> Expiry Date: {}".format(auth_cookie, expiry))
            #     www_response.set_cookie("auth_token", auth_cookie, expires=expiry)

            #     return www_response
        else:
            status = "incomplete"


    return render(request, 'CavTutor/search.html', {
            'results': {},
            'form': search_form,
            'status': status})
