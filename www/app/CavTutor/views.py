from django.shortcuts import render
#from django.core.urlresolvers import reverse
#from django.http.response import HttpResponse, HttpResponseRedirect
#import requests
#from core.settings import UX_BASE 
#import json

"""
    Index page
"""
def index(request):

    context = {
            "title" : "CavTutor: A Tutoring Marketplace",
            "models" : ['institutions', 'users', 'courses', 'tutors', 'tutees'],
        }

    return render(request, 'CavTutor/index.html', context)

# vim: ai ts=4 sts=4 et sw=4
