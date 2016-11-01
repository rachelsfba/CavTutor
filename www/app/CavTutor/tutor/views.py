# views for the Tutor model
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from rest_framework import status

from CavTutor.decorators import login_required, nologin_required, _get_loggedin_user
from core.settings import UX_BASE 
from CavTutor.tutor.forms import *
import requests
import json

def listings(request):

    json_data = urlopen(UX_BASE + 'tutors/').read().decode('utf-8')
    context = {'tutors' : json.loads(json_data) }

    return render(request, 'CavTutor/tutor-list.html', context)

def detail(request, tutor_id):
    try:
        json_data = urlopen(UX_BASE + 'tutors/' + tutor_id).read().decode('utf-8')
        context = {'tutor' : json.loads(json_data) }
        return render(request, 'CavTutor/tutor-detail.html', context)
    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "tutor",
                "id": tutor_id,
            })

# vim: ai ts=4 sts=4 et sw=4
def _tutor_register_ux(user_id, course_id, adv_rate):
    data = {
            'user': user_id,
            'course': course_id,
            'adv_rate': adv_rate
        }

    request = requests.post(UX_BASE + 'tutors/create/', data=data)
    print(request)
    if request.status_code == 200 or request.status_code == 201:
        return request.json()
    return 

@login_required 
def tutor_new(request):

    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        register_form = TutorRegisterForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        register_form = TutorRegisterForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if register_form.is_valid():
            # Redirect to index page after successful login.
            #next_page = reverse('index')
            # Retrieve login response 
            postdata  =dict(request.POST)

            course_id= str(postdata['course'][0])
            user_id = str(_get_loggedin_user(request)['id'])
            adv_rate = str(postdata['adv_rate'][0])

            ux_register_response = _tutor_register_ux(user_id, course_id, adv_rate)
            print(ux_register_response)
            if ux_register_response:
                next_page = reverse('tutor-detail', kwargs={"tutor_id": ux_register_response['id']})
            else:
                next_page = reverse('tutor-create')

            if not ux_register_response:
                # ux layer said the form was invalid;
                # probably means a user already exists with that username or email
                status = "invalid" 
            else:
                www_response = HttpResponseRedirect(next_page)
                return www_response
                #return render(request, 'CavTutor/index.html', {
                #        'username': request.POST.get('username'),
                #   })
        else:
            status = "incomplete"

    return render(request, 'CavTutor/tutor-register.html', {
            'form': register_form,
            'status': status,
        })
