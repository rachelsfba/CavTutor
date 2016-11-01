"""
 Namespace: CavTutor.institution.views

 Description: Contains views for the Institution model
"""

# Allows us to render a template
from django.shortcuts import render

# Allows us to do reverse lookup URI resolution
from django.core.urlresolvers import reverse

# Allow us to perform a redirect instead of rendering a template
from django.http.response import HttpResponseRedirect

# DRF has a list of HTTP status codes in rest_framework.status
from rest_framework import status

# Retrieve base experience-layer URL prefix from core.settngs
from core.settings import UX_BASE 

# Get our login_required decorator to make things easier on us
from CavTutor.decorators import login_required

# Get our forms to create a new record
from CavTutor.institution.forms import *

# Get some RESTful libraries
import requests, json

@login_required
def create(request):
    # Assume we have a good form.
    state = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        inst_form = InstitutionCreateForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        inst_form = InstitutionCreateForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if inst_form.is_valid():
            # Forms will sanitize for us

            # Retrieve login response 
            ux_response = _new_listing_ux(request.POST)

            if not ux_response:# or not ux_response['token']:
                state = "incorrect"
            else:
                # Yay! We succeeded in creating the new record.

                # Redirect to the new object!
                next_page = reverse('institution-detail', kwargs={"inst_id": ux_response['id']})

                www_response = HttpResponseRedirect(next_page)
                return www_response
        else:
            state = "incomplete"

    return render(request, 'CavTutor/institution-create.html', {
            'form': inst_form,
            'status': state,
        })

    # json_data = urlopen(UX_BASE + 'institutions_new/').read().decode('utf-8')
    # context = {'institutions' : json.loads(json_data) }

    # return render(request, 'CavTutor/institution-new.html', context)

def _new_listing_ux(postdata):

    request = requests.post(UX_BASE + 'institutions/create/', data=postdata)


    if request.status_code == status.HTTP_201_CREATED:
        return request.json()

    return 

def listings(request):

    inst_data = requests.get(UX_BASE + 'institutions/')

    context = {'institutions' : inst_data.json() }

    return render(request, 'CavTutor/institution-list.html', context)

def detail(request, inst_id):
    
    inst_data = requests.get(UX_BASE + 'institutions/' + inst_id)
    
    if inst_data.status_code == status.HTTP_200_OK:
        context = {'institution' : inst_data.json() }

        return render(request, 'CavTutor/institution-detail.html', context)

    return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
            "model": "instititution",
            "id": inst_id,
        })

# vim: ai ts=4 sts=4 et sw=4
