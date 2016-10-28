# views for the Course model
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

    json_data = urlopen(UX_BASE + 'courses/').read().decode('utf-8')
    context = {'courses' : json.loads(json_data), }

    return render(request, 'CavTutor/course-list.html', context)

def detail(request, course_id):
    try:
        course_json_data = urlopen(UX_BASE + 'courses/' + course_id).read().decode('utf-8')
        course_data = json.loads(course_json_data)

        context = {'course' : course_data,}
        return render(request, 'CavTutor/course-detail.html', context)
    except HTTPError as e:
        return render(request, 'CavTutor/generics/generic-item-not-found.html', status=404, context={
                "model": "course",
                "id": course_id,
            })

# vim: ai ts=4 sts=4 et sw=4
