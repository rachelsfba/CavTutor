from django.shortcuts import render

from django.http.response import HttpResponse
from urllib.request import urlopen

import requests
import json

API_BASE = 'http://api:8000/'

def institution_list(request):
#        json_data = urlopen(API_BASE + 'users/?format=json').read().decode('utf-8')
#        data = json.loads(json_data)

    json_data = urlopen(API_BASE + 'institutions/?format=json').read()

    return HttpResponse(json_data)

def institution_detail(request, inst_id):

    if request.method != "GET":
        return HttpResponse(statuscode=400)

    json_data = urlopen(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).read()
    return HttpResponse(json_data)
