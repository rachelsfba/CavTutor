from django.shortcuts import render
from urllib.request import urlopen

import json
#import requests

UX_BASE = 'http://ux:8000/'

# Create your views here.
def institution_list(request):

    json_data = urlopen(UX_BASE + 'institutions/').read().decode('utf-8')
    context = {'institutions' : json.loads(json_data) }

    return render(request, 'CavTutor/institution-list.html', context)

def institution_detail(request, inst_id):

    json_data = urlopen(UX_BASE + 'institutions/' + inst_id).read().decode('utf-8')
    context = {'institution' : json.loads(json_data) }

    return render(request, 'CavTutor/institution-detail.html', context)

