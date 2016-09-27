import datetime

from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict, fields_for_model
from django import db

from . import models

""" An abstract class representing a self object. """
class self(object):
    # internal method to output JSON indicating that an error has occurred
    def _error_response(result):
        return JsonResponse({'okay': False, 'result': result })

    # internal moethod to output JSON given that the requested operation was a success
    def _success_response(result):
        return JsonResponse({'okay': True, 'result': result })

    # unimplemented method used to create a new object
    def create(request):
        raise NotImplementedError("Child classes must implement create() before using the self class!")

    # unimplemented method meant to lookup an existing object
    def lookup(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the self class!")

    # unimplemented method meant to delete an existing object
    def delete(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the self class!")


""" Defines a User service API. """
class User(self):
    def create(request):
        if request.method != "POST":
            return self._error_response(result="Expected a POST request!")
        elif 'f_name' not in request.POST or \
            'l_name' not in request.POST or \
            'email' not in request.POST or \
            'password' not in request.POST or \
            'username' not in request.POST:
            return self._error_response(result="POST data is missing required fields!")
        else:
            new_user = models.User(
                username=request.POST['username'], \
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
                return self._error_response(result="An unknown database error has occurred.")

            return self._success_response(result={'id': new_user.id})

    def delete(request, id):
        if request.method != "GET":
            return self._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_user = models.User.objects.get(pk=id)
            except models.User.DoesNotExist:
                return self._error_response(result="A user matching id={} was not found.".format(id))

            lookup_user.delete()
            return self._success_response(result="User with id={} successfully removed!".format(id))

    def lookup(request, id):
        if request.method != "GET":
            return self._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_user = models.User.objects.get(pk=id)
            except models.User.DoesNotExist:
                return self._error_response(result="A user matching id={} was not found.".format(id))

            return self._success_response(result=model_to_dict(lookup_user, exclude="password"))

""" Defines an Institution services API. """
class Institution(self):
    def create(request):
        if request.method != "POST":
            return self._error_response(result="Expected a POST request!")
        elif 'name' not in request.POST or \
            'abbrv' not in request.POST or \
            'address' not in request.POST:
            return self._error_response(result="POST data is missing required fields!")
        else:
            new_inst = models.Institution(
                name=request.POST['name'], \
                abbrv=request.POST['abbrv'], \
                address=request.POST['address'], \
            )

            try:
                new_inst.save()
            except db.Error:
                return self._error_response(result="An unknown database error has occurred.")

            return self._success_response(result={'id': new_inst.id})

    def lookup(request, id):
        if request.method != "GET":
            return self._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_inst = models.Institution.objects.get(pk=id)
            except models.Institution.DoesNotExist:
                return self._error_response(result="An institution matching id={} was not found.".format(id))

            return self._success_response(result=model_to_dict(lookup_inst))
