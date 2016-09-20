import datetime

from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db

from . import models

def _error_response(req, msg):
    return JsonResponse({'okay':False,'result':msg })
def _success_response(req, msg):
    return JsonResponse({'okay':True,'result':msg })


#when adding a db entry which references the foreign key
#use the following construction in addition to checking for
#missing fields
"""
    try:
        giver = models.User.objects.get(pk=request.POST['giver_id'])
    except models.User.DoesNotExist:
        return _error_response(request, "giver not found")
    
    t = models.Thing(title=request.POST['title'],                       \
                     description = request.POST.get('description', ''), \
                     giver=giver,                                       \
                     location=request.POST['location'],                 \
                     date_given=datetime.datetime.now(),                \
                     was_taken=False                                    \
                     )
    try:
        t.save()
    except db.Error:
        return _error_response(request, "db error")
    return _success_response(request, {'thing_id': t.pk})

"""
def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'f_name' not in request.POST or     \
       'l_name' not in request.POST or     \
       'email' not in request.POST or   \
     'password' not in request.POST or   \
       'username' not in request.POST:
        return _error_response(request, "missing required fields")

    u = models.User(username=request.POST['username'],                         \
                    f_name=request.POST['f_name'],                             \
                    l_name=request.POST['l_name'],                             \
                    password=hashers.make_password(request.POST['password']),  \
                    email=request.POST['email'],                               \
                    date_joined=datetime.datetime.now()                        \
                    )

    try:
        u.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'user_id': u.pk})

def lookup_user(request, user_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'username': u.username,      \
                                       'f_name': u.f_name,          \
                                       'l_name': u.l_name,          \
                                       'email': u.email,            \
                                       'date_joined': u.date_joined \
                                       })
