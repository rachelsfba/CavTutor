from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from rest_framework import status

from .forms import *

import json


UX_BASE = 'http://ux:8000/'


def index(request):

    context = {
            "title" : "CavTutor: A Tutoring Marketplace",
            "models" : ['institutions', 'users', 'courses', 'tutors', 'tutees'],
        }

    return render(request, 'CavTutor/index.html', context)


"""
    Institutions
"""

def institution_list(request):

    json_data = urlopen(UX_BASE + 'institutions/').read().decode('utf-8')
    context = {'institutions' : json.loads(json_data) }

    return render(request, 'CavTutor/institution-list.html', context)

def institution_detail(request, inst_id):
    try: 
        json_data = urlopen(UX_BASE + 'institutions/' + inst_id).read().decode('utf-8')
        context = {'institution' : json.loads(json_data) }

        return render(request, 'CavTutor/institution-detail.html', context)

    except HTTPError as e:
        return render(request, '404.html', status=404, context={
                "model": "instititution",
                "id": inst_id,
            })

"""
    Course
"""
def course_list(request):

    json_data = urlopen(UX_BASE + 'courses/').read().decode('utf-8')
    context = {'courses' : json.loads(json_data), }

    return render(request, 'CavTutor/course-list.html', context)

def course_detail(request, course_id):
    try:
        course_json_data = urlopen(UX_BASE + 'courses/' + course_id).read().decode('utf-8')
        course_data = json.loads(course_json_data)

        context = {'course' : course_data,}
        return render(request, 'CavTutor/course-detail.html', context)
    except HTTPError as e:
        return render(request, '404.html', status=404, context={
                "model": "course",
                "id": course_id,
            })

"""
    Tutor
"""
def tutor_list(request):

    json_data = urlopen(UX_BASE + 'tutors/').read().decode('utf-8')
    context = {'tutors' : json.loads(json_data) }

    return render(request, 'CavTutor/tutor-list.html', context)

def tutor_detail(request, tutor_id):
    try:
        json_data = urlopen(UX_BASE + 'tutors/' + tutor_id).read().decode('utf-8')
        context = {'tutor' : json.loads(json_data) }
        return render(request, 'CavTutor/tutor-detail.html', context)
    except HTTPError as e:
        return render(request, '404.html', status=404, context={
                "model": "tutor",
                "id": tutor_id,
            })

"""
    Tutee
"""
def tutee_list(request):

    json_data = urlopen(UX_BASE + 'tutees/').read().decode('utf-8')
    context = {'tutees' : json.loads(json_data) }

    return render(request, 'CavTutor/tutee-list.html', context)

def tutee_detail(request, tutee_id):
    try:
        json_data = urlopen(UX_BASE + 'tutees/' + tutee_id).read().decode('utf-8')
        context = {'tutee' : json.loads(json_data) }

        return render(request, 'CavTutor/tutee-detail.html', context)
    except HTTPError as e:
        return render(request, '404.html', status=404, context={
                "model": "tutee",
                "id": tutee_id,
            })

"""
    User
"""
def user_list(request):

    json_data = urlopen(UX_BASE + 'users/').read().decode('utf-8')
    context = {'users' : json.loads(json_data) }

    return render(request, 'CavTutor/user-list.html', context)

def user_detail(request, user_id):
    try:
        json_data = urlopen(UX_BASE + 'users/' + user_id).read().decode('utf-8')
        context = {'user' : json.loads(json_data) }

        return render(request, 'CavTutor/user-detail.html', context)
    except HTTPError as e:
        return render(request, '404.html', status=404, context={
                "model": "user",
                "id": user_id,
            })

@csrf_protect
def user_login(request):
    
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

            if not ux_response or not ux_response['user_id']:
                status = "incorrect"
            else:
                auth_cookie = ux_response['auth_cookie']
                
                www_response = HttpReponseRedirect(next_page)
                www_response.set_cookie("auth_cookie", auth_cookie)
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
        return {}, 404

    return json.loads(request.read().decode('utf-8')), request.getcode()
                                                                                        
# vim: ai ts=4 sts=4 et sw=4
