"""
    MODULE:
    CavTutor.user.views
    
    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for User objects.
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

from CavTutor.tutor import views as tutor_views
from CavTutor.tutee import views as tutee_views

# List of all user objects
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest()

    users = requests.get(API_BASE + 'users/?format=json')

    if users.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    return HttpResponse(users.text)

# Details a specific user object
def detail(request, user_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    users = requests.get(API_BASE + 'users/{}/?format=json'.format(user_id))

    if users.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    data = users.json()

    # add two additional boolean fields to what the API gave us
    data['is_tutor'] = _user_is_tutor(int(user_id))
    data['is_tutee'] = _user_is_tutee(int(user_id))

    return HttpResponse(json.dumps(data))


def tutor_listings(request, user_id):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    tutor_data = requests.get(API_BASE + 'tutors/?format=json')
    
    if tutor_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutor_data_parsed = []

    for tutor in tutor_data.json():
        if str(tutor['user']) == user_id:
            tutor_data_parsed.append(tutor_views._tutor_foreign_key_id_to_json(tutor))
    
    return HttpResponse(json.dumps(tutor_data_parsed))

def tutee_listings(request, user_id):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    tutee_data = requests.get(API_BASE + 'tutees/?format=json')
    
    if tutee_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    
    tutee_data_parsed = []

    for tutee in tutee_data.json():
        if str(tutee['user']) == user_id:
            tutee_data_parsed.append(tutee_views._tutee_foreign_key_id_to_json(tutee))
    
    return HttpResponse(json.dumps(tutee_data_parsed))




def _user_is_tutee(user_id):
    tutees = requests.get(API_BASE + 'tutees/?format=json')

    for record in tutees.json():
        if record['user'] == user_id:
            return True
    return False

def _user_is_tutor(user_id):
    tutors = requests.get(API_BASE + 'tutors/?format=json')

    for record in tutors.json():
        if record['user'] == user_id:
            return True
    return False
