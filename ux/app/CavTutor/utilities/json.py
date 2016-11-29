""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """

import requests, json

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status


from core.settings import UX_BASE

def _unflatten(item_dict):
    new_dict = {}

    for key, value in item_dict.items():
        if "user:" not in key and "course:" not in key:
            new_dict[key] = value

    new_dict = _tutor_foreign_key_id_to_json(new_dict)

    return new_dict

def _tutor_foreign_key_id_to_json(tutor):
    # Should throw an error if a field is missing from the model
    user_data = requests.get(UX_BASE + 'users/{}/'.format(tutor['user']))
    course_data = requests.get(UX_BASE + 'courses/{}/'.format(tutor['course']))

    if (user_data.status_code, course_data.status_code) != (status.HTTP_200_OK,) * 2:
        return KeyError('User or Course not defined')

    tutor['user'] = user_data.json()
    tutor['course'] = course_data.json()

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    del tutor['user']['password']

    return tutor

def _tutor_foreign_key_id_to_json_v2(tutor, user_list, course_list):
    # Should throw an error if a field is missing from the model
    user_id = tutor['user']
    course_id = tutor['course']


    user_data = [user_json for user_json in user_list if user_json['id'] == user_id][0]
    course_data = [course_json for course_json in course_list if course_json['id'] == course_id][0]

    tutor['user'] = user_data
    tutor['course'] = course_data

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    #del tutor['user']['password']

    return tutor



def _flatten(tutor):
    user_data = requests.get(API_BASE + 'users/{}/'.format(tutor['user']))
    course_data = requests.get(API_BASE + 'courses/{}/'.format(tutor['course']))

    if (user_data.status_code, course_data.status_code) != (status.HTTP_200_OK,) * 2:
        return []

    for field_name, field_val in user_data.json().items():
        tutor['user:' + field_name] = field_val
    for field_name, field_val in course_data.json().items():
        tutor['course:' + field_name] = field_val

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    del tutor['user:password']

    return tutor

