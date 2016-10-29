# views for the Institution model
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from rest_framework import status

from core.settings import UX_BASE 

import json

def listings(request):

    json_data = urlopen(UX_BASE + 'institutions/').read().decode('utf-8')
    context = {'institutions' : json.loads(json_data) }

    return render(request, 'CavTutor/institution-list.html', context)

def detail(request, inst_id):
    try:
        json_data = urlopen(UX_BASE + 'institutions/' + inst_id).read().decode('utf-8')
        context = {'institution' : json.loads(json_data) }

        return render(request, 'CavTutor/institution-detail.html', context)

    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "instititution",
                "id": inst_id,
            })

# vim: ai ts=4 sts=4 et sw=4
