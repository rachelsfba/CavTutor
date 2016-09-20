"""
N.B. When adding a service to create a new model with a foreign key, we must
first check if an objects exists with the given foreign key. We may use the
following construction (in addition to other checks such as checking for
missing fields).

try:
    giver = models.User.objects.get(pk=request.POST['giver_id'])
except models.User.DoesNotExist:
    return _error_response(request, result="giver not found")

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
    return _error_response(request, result="db error")
return _success_response(request, result={'thing_id': t.pk})

"""
import datetime

from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db

from . import models

# Should move this basic class to /app/isa_app/isa_app/services.py perhaps?

""" An abstract class representing a Service object. """
class Service(object):
    # internal method to output JSON indicating that an error has occurred
    def _error_response(request, result):
        return JsonResponse({'okay': False, 'result': result })

    # internal moethod to output JSON given that the requested operation was a success
    def _success_response(request, result):
        return JsonResponse({'okay': True, 'result': result })

    # unimplemented method used to create a new object
    def create(request):
        raise NotImplementedError("Child classes must implement create() before using the Service class!")

    # unimplemented method meant to lookup an existing object
    def lookup(request):
        raise NotImplementedError("Child classes must implement lookup() before using the Service class!")

""" Defines a User service API. """
class User(Service):
    def create(request):
        if request.method != "POST":
            return Service._error_response(request, result="Expected a POST request!")
        elif 'f_name' not in request.POST or \
            'l_name' not in request.POST or \
            'email' not in request.POST or \
            'password' not in request.POST or \
            'username' not in request.POST:
            return Service._error_response(request, result="POST data is missing required fields!")
        else:
            new_user = models.User(username=request.POST['username'], \
                f_name=request.POST['f_name'], \
                l_name=request.POST['l_name'], \
                # use Django hashing algorithms to store a new password
                password=hashers.make_password(request.POST['password']), \
                email=request.POST['email'], \
                date_joined=datetime.datetime.now(), \
            )

            try:
                new_user.save()
            except db.Error:
                return Service._error_response(request, result="An unknown database error has occurred.")

            return Service._success_response(request, result={'user_id': new_user.id})

    def lookup(request, user_id=1):
        if request.method != "GET":
            return Service._error_response(request, result="Expected a GET request!")
        else:
            try:
                lookup_user = models.User.objects.get(pk=user_id)
            except models.User.DoesNotExist:
                return Service._error_response(request, result="A user matching id={} was not found.".format(user_id))

            return Service._success_response(request, result={'username': lookup_user.username, \
                'f_name': lookup_user.f_name, \
                'l_name': lookup_user.l_name, \
                'email': lookup_user.email, \
                'date_joined': lookup_user.date_joined \
            })
