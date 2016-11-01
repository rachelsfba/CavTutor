"""
    MODULE:
    CavTutor.institution.views
    
    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for Institution objects.
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

# List of all institution objects
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest()
    
    data = requests.get(API_BASE + 'institutions/?format=json')

    if data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    return HttpResponse(data.text)

# Details a specific institution object
def detail(request, inst_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    json_data = requests.get(API_BASE + 'institutions/{}/?format=json'.format(inst_id))
    
    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    data = json_data.json()
    data['num_courses'] = get_institution_num_courses(int(inst_id))

    return HttpResponse(json.dumps(data))


def get_institution_name(inst_id):
    data = requests.get(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).json()

    return data['name']

def get_institution_num_courses(inst_id):

    courses_data = requests.get(API_BASE + 'courses/?format=json').json()

    count = 0

    for course in courses_data:
        if course['institution'] == int(inst_id):
            count += 1

    return count

def create(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest()

    # attempt to get a list of all obects from the API, so we can see if the
    # given info already exists in our system
    inst_list = requests.get(API_BASE + 'institutions/?format=json')

    if inst_list.status_code != 200:
        # If users listing didn't work for some reason, 
        return HttpResponseServerError()
    
    # we have to iterate over all the institutions in the entire listing. need to find
    # a more RESTful and efficient way
    for inst in inst_list.json():
        # for every institution, match the POSTed name with this record's name
        # to check for duplicates
        if request.POST.get('name') == inst['name']:
            # uh-oh, it already exists in system
            return HttpResponseBadRequest()
    
    # If it wasn't found in the database already, send a POST request with the needed info.
    new_inst_data = requests.post(API_BASE + 'institutions/', data=request.POST)

    if new_inst_data.status_code != 201:
        return HttpResponseServerError()

    return HttpResponse(new_inst_data.text, status=201)


