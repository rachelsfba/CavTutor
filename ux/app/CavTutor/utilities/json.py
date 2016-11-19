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

