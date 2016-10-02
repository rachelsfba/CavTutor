import datetime

from django.http import JsonResponse
from django import db
from django.contrib.auth import hashers
from django.forms import ValidationError
from django.forms.models import model_to_dict, fields_for_model
from django.core.validators import validate_email


from . import models

""" An abstract class representing a Service object. """
class Service(object):
    # internal method to output JSON indicating that an error has occurred
    def _error_response(result):
        return JsonResponse({'okay': False, 'result': result })

    # internal moethod to output JSON given that the requested operation was a success
    def _success_response(result):
        return JsonResponse({'okay': True, 'result': result })

    # unimplemented method used to create a new object
    def create(request):
        raise NotImplementedError("Child classes must implement create() before using the Service class!")

    # unimplemented method meant to lookup an existing object
    def lookup(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the Service class!")

    # unimplemented method meant to delete an existing object
    def delete(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the Service class!")

    def update(request, id):
        raise NotImplementedError("Child classes must implement update() before using the Service class!")

""" Defines an Institution services API. """
class Institution(Service):

    def update(request, id):
        if request.method != "POST":
            return Service._error_response(result="Expected a POST request!")

        try:
            lookup_inst = models.Institution.objects.get(pk=id)
        except models.Institution.DoesNotExist:
            return Service._error_response(result="An institution matching id={} was not found.".format(id))

        changed_fields = {}

        if 'name' in request.POST and lookup_inst.name != request.POST['name']:
            lookup_inst.name = request.POST['name']
            changed_fields['name'] = request.POST['name']

        if 'abbrv' in request.POST and lookup_inst.abbrv != request.POST['abbrv']:
            lookup_inst.abbrv = request.POST['abbrv']
            changed_fields['abbrv'] = request.POST['abbrv']

        if 'address' in request.POST and lookup_inst.address != request.POST['address']:
            lookup_inst.address = request.POST['address']
            changed_fields['address'] = request.POST['address']

        if changed_fields:
            lookup_inst.save()
            return Service._success_response(result={'changed_fields': changed_fields})
        else:
            return Service._error_response(result="No fields were changed!")

    def create(request):
        if request.method != "POST":
            return Service._error_response(result="Expected a POST request!")
        elif 'name' not in request.POST or \
            'abbrv' not in request.POST or \
            'address' not in request.POST:
            return Service._error_response(result="POST data is missing required fields!")
        else:
            new_inst = models.Institution(
                name=request.POST['name'], \
                abbrv=request.POST['abbrv'], \
                address=request.POST['address'], \
            )

            try:
                new_inst.save()
            except db.Error:
                return Service._error_response(result="An unknown database error has occurred.")

            return Service._success_response(result={'id': new_inst.id})

    def delete(request, id):
        if request.method != "GET":
            return Service._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_inst = models.Institution.objects.get(pk=id)
            except models.Institution.DoesNotExist:
                return Service._error_response(result="An institution matching id={} was not found.".format(id))

            lookup_inst.delete()
            return Service._success_response(result="Institution with id={} successfully removed!".format(id))


    def lookup(request, id):
        if request.method != "GET":
            return Service._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_inst = models.Institution.objects.get(pk=id)
            except models.Institution.DoesNotExist:
                return Service._error_response(result="An institution matching id={} was not found.".format(id))

            return Service._success_response(result=model_to_dict(lookup_inst))

""" Defines a User service API. """
class User(Service):

    def update(request, id):
        if request.method != "POST":
            return Service._error_response(result="Expected a POST request!")

        try:
            lookup_user = models.User.objects.get(pk=id)
        except models.User.DoesNotExist:
            return Service._error_response(result="A user matching id={} was not found.".format(id))

        changed_fields = {}

        if 'username' in request.POST and lookup_user.username != request.POST['username']:
            lookup_user.username = request.POST['username']
            changed_fields['username'] = request.POST['username']
        if 'f_name' in request.POST and lookup_user.f_name != request.POST['f_name']:
            lookup_user.f_name = request.POST['f_name']
            changed_fields['f_name'] = request.POST['f_name']
        if 'l_name' in request.POST and lookup_user.l_name != request.POST['l_name']:
            lookup_user.l_name = request.POST['l_name']
            changed_fields['l_name'] = request.POST['l_name']
        if 'password' in request.POST and lookup_user.password != request.POST['password']:
            lookup_user.password = request.POST['password']
            changed_fields['password'] = request.POST['password']
        if 'email' in request.POST and lookup_user.email != request.POST['email']:
            try:
                validate_email(request.POST['email'])
            except ValidationError:
                return Service._error_response(result="Given an invalid email!")

            lookup_user.email = request.POST['email']
            changed_fields['email'] = request.POST['email']

        if changed_fields:
            lookup_user.save()
            return Service._success_response(result={'changed_fields': changed_fields})
        else:
            return Service._error_response(result="No fields were changed!")

    def create(request):
        if request.method != "POST":
            return Service._error_response(result="Expected a POST request!")
        elif 'f_name' not in request.POST or \
            'l_name' not in request.POST or \
            'email' not in request.POST or \
            'password' not in request.POST or \
            'username' not in request.POST:
            return Service._error_response(result="POST data is missing required fields!")
        else:
            try:
                validate_email(request.POST['email'])
            except ValidationError:
                return Service._error_response(result="Given an invalid email!")

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
                return Service._error_response(result="An unknown database error has occurred.")

            return Service._success_response(result={'id': new_user.id})

    def delete(request, id):
        if request.method != "GET":
            return Service._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_user = models.User.objects.get(pk=id)
            except models.User.DoesNotExist:
                return Service._error_response(result="A user matching id={} was not found.".format(id))

            lookup_user.delete()
            return Service._success_response(result="User with id={} successfully removed!".format(id))

    def lookup(request, id):
        if request.method != "GET":
            return Service._error_response(result="Expected a GET request!")
        else:
            try:
                lookup_user = models.User.objects.get(pk=id)
            except models.User.DoesNotExist:
                return Service._error_response(result="A user matching id={} was not found.".format(id))

            return Service._success_response(result=model_to_dict(lookup_user, exclude="password"))

