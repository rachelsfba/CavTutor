from django.shortcuts import render

from django.http.response import HttpResponse
from urllib.request import urlopen

import requests
import json

API_BASE = 'http://api:8000/'
"""
    Institutions
"""
# List of all institution objects
def institution_list(request):
    json_data = urlopen(API_BASE + 'institutions/?format=json').read()

    return HttpResponse(json_data)

# Details a specific institution object
def institution_detail(request, inst_id):
    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).read()
    return HttpResponse(json_data)

"""
    Users
"""
# List of all user objects
def user_list(request):
    json_data = urlopen(API_BASE + 'users/?format=json').read()

    return HttpResponse(json_data)

# Details a specific user object
def user_detail(request, user_id):
    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'users/{}/?format=json'.format(user_id)).read()
    return HttpResponse(json_data)

"""
    Tutors
"""
# List of all tutors
def tutor_list(request):
    json_data = urlopen(API_BASE + 'tutors/?format=json').read()

    return HttpResponse(json_data)

# Details a specific tutor
def tutor_detail(request, tutor_id):
    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'tutors/{}/?format=json'.format(tutor_id)).read()
    return HttpResponse(json_data)

"""
    Tutees
"""
# List of all tutees
def tutee_list(request):
    json_data = urlopen(API_BASE + 'tutees/?format=json').read()

    return HttpResponse(json_data)

# Details a specific tutee
def tutee_detail(request, tutee_id):
    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'tutees/{}/?format=json'.format(tutee_id)).read()
    return HttpResponse(json_data)

"""
    Courses
"""
# List of all courses
def course_list(request):
    json_data = urlopen(API_BASE + 'courses/?format=json').read()

    return HttpResponse(json_data)

# Details a specific course
def course_detail(request, course_id):
    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'courses/{}/?format=json'.format(course_id)).read()
    return HttpResponse(json_data)

