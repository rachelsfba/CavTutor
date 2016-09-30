from django.http import JsonResponse

# commenting out for now, might need later!
#from django.forms.models import model_to_dict, fields_for_model
#from django import db

#import CavTutor.models

__all__ = ['users', 'institutions']

#users = 'CavTutor.services.users.User'
#institutions = 'CavTutor.services.institutions.Institutions'

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
        raise NotImplementedError("Child classes must implement create() before using the self class!")

    # unimplemented method meant to lookup an existing object
    def lookup(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the self class!")

    # unimplemented method meant to delete an existing object
    def delete(request, id):
        raise NotImplementedError("Child classes must implement lookup() before using the self class!")
