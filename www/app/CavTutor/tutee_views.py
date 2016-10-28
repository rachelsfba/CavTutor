# views for the Tutee model
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from rest_framework import status

from core.settings import UX_BASE 
from .forms import *

import json

def listings(request):

    json_data = urlopen(UX_BASE + 'tutees/').read().decode('utf-8')
    context = {'tutees' : json.loads(json_data) }

    return render(request, 'CavTutor/tutee-list.html', context)

def detail(request, tutee_id):
    try:
        json_data = urlopen(UX_BASE + 'tutees/' + tutee_id).read().decode('utf-8')
        context = {'tutee' : json.loads(json_data) }

        return render(request, 'CavTutor/tutee-detail.html', context)
    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "tutee",
                "id": tutee_id,
            })

# vim: ai ts=4 sts=4 et sw=4
