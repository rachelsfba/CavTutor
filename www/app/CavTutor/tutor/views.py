# views for the Tutor model
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from rest_framework import status

from CavTutor.decorators import login_required, nologin_required, _get_loggedin_user
from CavTutor.tutor.forms import *

from core.settings import UX_BASE

import requests, json

def listings(request):

    json_data = requests.get(UX_BASE + 'tutors/').json()
    context = {'tutors' : json_data }

    return render(request, 'CavTutor/tutor-list.html', context)

def detail(request, tutor_id):
    json_data = requests.get(UX_BASE + 'tutors/' + tutor_id)
    context = {'tutor' : json_data.json() }

    if json_data.status_code == status.HTTP_200_OK:
        return render(request, 'CavTutor/tutor-detail.html', context)

    return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
            "model": "tutor",
            "id": tutor_id,
        })

@login_required
def create(request):

    # Assume we have a good form.
    status = "ok"

    # If the user didn't POST anything, they probably haven't filled out the
    # form yet. Let's give them a blank one to fill in.
    if request.method == 'GET':
        # Create new login form and render it.
        _form = TutorCreateForm()

    # Otherwise they must have given us something as POST data. Let's try to
    # validate that.
    else:
        # Create a new Django form based on POST data.
        _form = TutorCreateForm(request.POST)

        # If all fields were filled in, let's try to validate that info against
        # our database.
        if _form.is_valid():

            course = request.POST.get('course')
            adv_rate = request.POST.get('rate')

            user = _get_loggedin_user(request)['id']

            ux_response = _tutor_register_ux(user, course, adv_rate)

            if ux_response:
                next_page = reverse('tutor-detail', kwargs={"tutor_id": ux_response['id']})

                return HttpResponseRedirect(next_page)
            else:
                # ux layer said the form was invalid;
                # probably means that tutor record already exists
                status = "invalid"
        else:
            status = "incomplete"

    return render(request, 'CavTutor/tutor-create.html', {
            'form': _form,
            'status': status,
        })

def search(request):

    search_response = None

    if not request.GET.get('query'):
        search_form = TutorSearchForm()
    else:
        # Create a new Django form based on POST data.
        search_form = TutorSearchForm(request.GET)

    # If all fields were filled in, let's try to validate that info against
    # our database.
    if search_form.is_valid():
        # Forms will sanitize for us
        search_response = requests.get(UX_BASE + 'tutors/search/', params=search_form.cleaned_data).json()

    return render(request, 'CavTutor/tutor-search.html', {
            'results': search_response,
            'form': search_form,
        })


def _tutor_register_ux(user_id, course_id, adv_rate):
    data = {
            'user': user_id,
            'course': course_id,
            'adv_rate': adv_rate
        }

    request = requests.post(UX_BASE + 'tutors/create/', data=data)

    if request.status_code == 201:
        return request.json()
    return

# vim: ai ts=4 sts=4 et sw=4
