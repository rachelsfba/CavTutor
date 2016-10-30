# views for the Institution model
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
from CavTutor.decorators import login_required

from .forms import *
import requests

@login_required
def institution_new(request):
    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        newinstitution_form = InstitutionNewForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        newinstitution_form = InstitutionNewForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if newinstitution_form.is_valid():
            # Forms will sanitize for us

            # Redirect to index page after successful new listing
            # ideally redirect to the new listing itself, (how do you know the url before its created though?)
            next_page = reverse('index')

            # Retrieve login response 
            ux_response = _new_listing_ux(request.POST)

            if not ux_response:# or not ux_response['token']:
                status = "incorrect"
            else:
                #dont need these for a new listing??
                # auth_cookie = ux_response['token']
                # expiry = ux_response['expiry_date']
                www_response = HttpResponseRedirect(next_page)
                return www_response
        else:
            status = "incomplete"

    return render(request, 'CavTutor/institution-new.html', {
            'form': newinstitution_form,
            'status': status,
        })

    # json_data = urlopen(UX_BASE + 'institutions_new/').read().decode('utf-8')
    # context = {'institutions' : json.loads(json_data) }

    # return render(request, 'CavTutor/institution-new.html', context)

def _new_listing_ux(postdata):

    request = requests.post(UX_BASE + 'institutions_new/', data=postdata)


    if request.status_code == 201:
        return request.json()

    return 

def listings(request):

    json_data = urlopen(UX_BASE + 'institutions/').read().decode('utf-8')
    context = {'institutions' : json.loads(json_data) }

    return render(request, 'CavTutor/institution-list.html', context)

def detail(request, inst_id):
    try:
        json_data = urlopen(UX_BASE + 'institutions/' + inst_id).read().decode('utf-8')
        context = {'institution' : json.loads(json_data) }

        return render(request, 'CavTutor/institution-detail.html', context)

    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "instititution",
                "id": inst_id,
            })

# vim: ai ts=4 sts=4 et sw=4
