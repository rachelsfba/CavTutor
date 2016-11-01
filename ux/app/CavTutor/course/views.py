"""
    MODULE:
    CavTutor.course.views
    
    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for Course objects.
"""

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """
import requests, json 

""" These libraries are needed for cookie token generation. """
import os, hmac

""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE

"""  We utilize some common Django idioms, so fetch those implementations. """
from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status

from CavTutor.institution import views as institution_views

# List of all courses
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    courses = requests.get(API_BASE + 'courses/?format=json')

    if courses.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    courses_parsed = []

    for course in courses.json():
        course['num_tutors'] = get_course_num_tutors(course['id'])
        course['institution_name'] = institution_views.get_institution_name(course['institution'])

        courses_parsed.append(course)

    return HttpResponse(json.dumps(courses_parsed))


# Details a specific course
def detail(request, course_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    course = requests.get(API_BASE + 'courses/{}/?format=json'.format(course_id))

    if course.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    data = course.json()
    data['num_tutors'] = get_course_num_tutors(course_id)
    data['institution_name'] = institution_views.get_institution_name(data['institution'])

    return HttpResponse(json.dumps(data))


def get_course_num_tutors(course_id):
    
    tutors = requests.get(API_BASE + 'tutors/?format=json')
    tutors_data = tutors.json()
    
    tutor_counter = 0
    for tutor in tutors_data:
        if tutor['course'] == int(course_id):
            tutor_counter += 1
    return tutor_counter

