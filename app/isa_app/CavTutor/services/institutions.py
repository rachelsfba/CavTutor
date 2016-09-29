import datetime

from django.contrib.auth import hashers
from django.forms.models import model_to_dict, fields_for_model
from django import db

import CavTutor.models
from CavTutor.services import Service

""" Defines an Institution services API. """
class Institution(Service):
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
