import datetime

from django.forms.models import model_to_dict, fields_for_model
from django import db

import CavTutor.models
from CavTutor.services import Service

""" Defines a User service API. """
class User(Service):
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

