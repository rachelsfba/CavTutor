"""
    MODULE:
    CavTutor.tutor.views
    
    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for Tutor objects.
"""

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """
import requests, json 

""" These libraries are needed for cookie token generation. """
import os, hmac

""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE, UX_BASE

"""  We utilize some common Django idioms, so fetch those implementations. """
from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status

# List of all tutors
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    tutor_data = requests.get(API_BASE + 'tutors/?format=json')
    
    if tutor_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutor_data_parsed = []

    for tutor in tutor_data.json():
        tutor_data_parsed.append(_tutor_foreign_key_id_to_json(tutor))
    
    return HttpResponse(json.dumps(tutor_data_parsed))

# Details a specific tutor
def detail(request, tutor_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    json_data = requests.get(API_BASE + 'tutors/{}/?format=json'.format(tutor_id))

    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutor_data = _tutor_foreign_key_id_to_json(json_data.json())
    tutor_data['num_tutees'] = get_tutor_num_tutees(tutor_id)

    return HttpResponse(json.dumps(tutor_data))

def _tutor_foreign_key_id_to_json(tutor):
    user_data = requests.get(UX_BASE + 'users/{}/'.format(tutor['user'])) 
    course_data = requests.get(UX_BASE + 'courses/{}/'.format(tutor['course']))
    
    tutor['user'] = user_data.json()
    tutor['course'] = course_data.json()
    
    return tutor

def get_tutor_num_tutees(tutor_id):
    tutee_data = requests.get(API_BASE + 'tutees/?format=json')
    
    #can't return 404 from here :C
    #if tutor_data.status_code != status.HTTP_200_OK:
    #    return HttpResponseNotFound()
    
    tutee_counter = 0
    
    for tutee in tutee_data.json():
        if tutee['tutor'] == int(tutor_id):
            tutee_counter += 1
    
    return tutee_counter

