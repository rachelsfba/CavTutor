"""
    MODULE:
    CavTutor.tutee.views
    
    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for Tutee objects.
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

# List of all tutees
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    tutee_data = requests.get(API_BASE + 'tutees/?format=json')
    
    if tutee_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutee_data_parsed = []

    for tutee in tutee_data.json():
        tutee_data_parsed.append(_tutee_foreign_key_id_to_json(tutee))
    
    return HttpResponse(json.dumps(tutee_data_parsed))

# Details a specific tutee
def detail(request, tutee_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    json_data = requests.get(API_BASE + 'tutees/{}/?format=json'.format(tutee_id))

    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutee_data = _tutee_foreign_key_id_to_json(json_data.json())

    return HttpResponse(json.dumps(tutee_data))

def _tutee_foreign_key_id_to_json(tutee):
    user_data = requests.get(UX_BASE + 'users/{}/'.format(tutee['user'])) 
    course_data = requests.get(UX_BASE + 'courses/{}/'.format(tutee['course']))
    tutor_data = requests.get(UX_BASE + 'tutors/{}/'.format(tutee['tutor']))
    
    tutee['user'] = user_data.json()
    tutee['course'] = course_data.json()
    tutee['tutor'] = tutor_data.json()

    return tutee

