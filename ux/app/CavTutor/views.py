import os
import hmac
import json
import datetime

import core.settings as settings

from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password
from urllib.request import urlopen
from urllib.error import HTTPError

from urllib.parse import urlencode

from . import institution_views

API_VERSION = 'v2'

API_BASE = 'http://api:8000/api/' + API_VERSION + "/"
UX_BASE = 'http://localhost:8000/'

HTTP_ERROR_500 = json.dumps(dict(detail="HTTP 500 Error: Intersal Service Error"))

HTTP_ERROR_400 = json.dumps(dict(detail="HTTP 400 Error: Bad Request"))
HTTP_ERROR_404 = json.dumps(dict(detail="HTTP 404 Error: File Not Found"))
"""
    Users
"""
""
    Tutors
"""
# List of all tutors
def tutor_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        tutor_json = urlopen(API_BASE + 'tutors/?format=json').read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    tutor_data = json.loads(tutor_json)

    tutor_data_parsed = []

    for tutor in tutor_data:
        tutor_data_parsed.append(_tutor_foreign_key_id_to_json(tutor))

    return HttpResponse(json.dumps(tutor_data_parsed))

# Details a specific tutor
def tutor_detail(request, tutor_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'tutors/{}/?format=json'.format(tutor_id)).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    tutor_data = json.loads(json_data)

    tutor_data = _tutor_foreign_key_id_to_json(tutor_data)

    tutor_data['num_tutees'] = get_tutor_num_tutees(tutor_id)

    return HttpResponse(json.dumps(tutor_data))


def _tutor_foreign_key_id_to_json(tutor):
    user_json = urlopen(UX_BASE + 'users/{}/'.format(tutor['user'])).read().decode('utf-8')
    user_data = json.loads(user_json)

    course_json = urlopen(UX_BASE + 'courses/{}/'.format(tutor['course'])).read().decode('utf-8')
    course_data = json.loads(course_json)

    tutor['user'] = user_data
    tutor['course'] = course_data

    return tutor

def get_tutor_num_tutees(tutor_id):
    tutee_json = urlopen(API_BASE + 'tutees/?format=json').read().decode('utf-8')
    tutee_data = json.loads(tutee_json)

    tutee_counter = 0

    for tutee in tutee_data:
        if tutee['tutor'] == int(tutor_id):
            tutee_counter += 1

    return tutee_counter

"""
    Tutees
"""
# List of all tutees
def tutee_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'tutees/?format=json').read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    tutee_data = json.loads(json_data)

    parsed_tutee_data = []

    for tutee in tutee_data:
        parsed_tutee_data.append(_tutee_foreign_key_id_to_json(tutee))

    return HttpResponse(json.dumps(parsed_tutee_data))

# Details a specific tutee
def tutee_detail(request, tutee_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'tutees/{}/?format=json'.format(tutee_id)).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    tutee_data = json.loads(json_data)

    tutee_data = _tutee_foreign_key_id_to_json(tutee_data)

    return HttpResponse(json.dumps(tutee_data))

def _tutee_foreign_key_id_to_json(tutee):
    user_json = urlopen(UX_BASE + 'users/{}/'.format(tutee['user'])).read().decode('utf-8')
    user_data = json.loads(user_json)

    course_json = urlopen(UX_BASE + 'courses/{}/'.format(tutee['course'])).read().decode('utf-8')
    course_data = json.loads(course_json)

    tutor_json = urlopen(UX_BASE + 'tutors/{}/'.format(tutee['tutor'])).read().decode('utf-8')
    tutor_data = json.loads(tutor_json)

    tutee['user'] = user_data
    tutee['course'] = course_data
    tutee['tutor'] = tutor_data

    return tutee

"""
    Courses
"""
# List of all courses
def course_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'courses/?format=json').read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    data = json.loads(json_data)

    new_data = []
    for course in data:
        course['num_tutors'] = get_course_num_tutors(course['id'])
        course['institution_name'] = institution_views.get_institution_name(course['institution'])

        new_data.append(course)

    return HttpResponse(json.dumps(new_data))

# Details a specific course
def course_detail(request, course_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'courses/{}/?format=json'.format(course_id)).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    data = json.loads(json_data)

    data['num_tutors'] = get_course_num_tutors(course_id)
    data['institution_name'] = institution_views.get_institution_name(data['institution'])

    return HttpResponse(json.dumps(data))

def get_course_num_tutors(course_id):
    tutors_json = urlopen(API_BASE + 'tutors/?format=json').read().decode('utf-8')
    tutors_data = json.loads(tutors_json)

    tutor_counter = 0

    for tutor in tutors_data:
        if tutor['course'] == int(course_id):
            tutor_counter += 1

    return tutor_counter

