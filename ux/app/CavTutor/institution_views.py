import json, requests

from core.settings import API_BASE, UX_BASE

from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

from rest_framework import status

HTTP_ERROR_500 = json.dumps(dict(detail="HTTP 500 Error: Internal Service Error"))
HTTP_ERROR_400 = json.dumps(dict(detail="HTTP 400 Error: Bad Request"))
HTTP_ERROR_404 = json.dumps(dict(detail="HTTP 404 Error: File Not Found"))

# List of all institution objects
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)
    
    data = requests.get(API_BASE + 'institutions/?format=json')

    if data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound(HTTP_ERROR_404)

    return HttpResponse(data.text)


# Details a specific institution object
def detail(request, inst_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    json_data = requests.get(API_BASE + 'institutions/{}/?format=json'.format(inst_id))
    
    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound(HTTP_ERROR_404)

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
        return HttpResponseBadRequest(HTTP_ERROR_400)

    # attempt to get a list of all obects from the API, so we can see if the
    # given info already exists in our system
    inst_list = requests.get(API_BASE + 'institutions/?format=json')

    if inst_list.status_code != 200:
        # If users listing didn't work for some reason, 
        return HttpResponseServerError(HTTP_ERROR_500)
    
    # we have to iterate over all the institutions in the entire listing. need to find
    # a more RESTful and efficient way
    for inst in inst_list.json():
        # for every institution, match the POSTed name with this record's name
        # to check for duplicates
        if request.POST.get('name') == inst['name']:
            # uh-oh, it already exists in system
            return HttpResponseBadRequest(HTTP_ERROR_400)
    
    # If it wasn't found in the database already, send a POST request with the needed info.
    new_inst_data = requests.post(API_BASE + 'institutions/', data=request.POST)

    if new_inst_data.status_code != 201:
        return HttpResponseServerError(HTTP_ERROR_500)

    return HttpResponse(new_inst_data.text, status=201)


