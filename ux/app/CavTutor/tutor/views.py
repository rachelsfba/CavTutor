"""
    MODULE:
    CavTutor.tutor.views

    DESCRIPTION:
    Acts as a go-between for the user-facing and API layers for Tutor objects.
"""

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """

import requests, json

""" These libraries are needed for cookie token generation. """
import os, hmac

""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE, UX_BASE, ELASTIC_SEARCH_NUM_RESULTS, KAFKA_ADDR

"""  We utilize some common Django idioms, so fetch those implementations. """
from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status

""" We want to add new listings to a Kafka queue. """
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=KAFKA_ADDR)

""" We want to search all the tutor listings. """
from elasticsearch import Elasticsearch
elasticsearch = Elasticsearch([{'host': 'elasticsearch'}])


# List of all tutors
def listings(request):

    if request.method != "GET":
        return HttpResponseBadRequest()

    tutor_data = requests.get(API_BASE + 'tutors/?format=json')

    if tutor_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    tutor_data_parsed = []

    for tutor in tutor_data.json():
        tutor_data_parsed.append(_tutor_foreign_key_id_to_json(tutor))

    return HttpResponse(json.dumps(tutor_data_parsed))


def search(request):

    if request.method != "POST" or not request.POST.get('query'):
        return HttpResponseBadRequest()

    query_str = request.POST.get('query')

    search_result = elasticsearch.search(
            index='tutor-listing-indexer',
            body={
                'query': {
                    'query_string': {
                        'query': query_str,
                        }
                    },
                # Implement pagination algorithm at some point (e.g. first 25, second 25, etc. on page 1, 2, ...)
                'size': ELASTIC_SEARCH_NUM_RESULTS,
            })

    tutors_found = []
   # print(search_result)
    for tutor in search_result['hits']['hits']:
        if '_source' in tutor:
            tutor_json = _unflatten(tutor['_source'])
            tutors_found.append(tutor_json)

    # {'timed_out': False, 'hits': {'total': 1, 'hits': [{'_score': 0.10848885, '_index': 'listing_index', '_source': {'id': 42, 'description': 'This is a used Macbook Air in great condition', 'title': 'Used MacbookAir 13"'}, '_id': '42', '_type': 'listing'}], 'max_score': 0.10848885}, '_shards': {'successful': 5, 'total': 5, 'failed': 0}, 'took': 21}
    return HttpResponse(json.dumps(tutors_found))

def _unflatten(item_dict):
    new_dict = {}

    for key, value in item_dict.items():
        if "user:" not in key and "course:" not in key:
            new_dict[key] = value

    new_dict = _tutor_foreign_key_id_to_json(new_dict)

    return new_dict

def _flatten(tutor):
    user_data = requests.get(API_BASE + 'users/{}/'.format(tutor['user']))
    course_data = requests.get(API_BASE + 'courses/{}/'.format(tutor['course']))

    if (user_data.status_code, course_data.status_code) != (status.HTTP_200_OK,) * 2:
        return "???"

    for field_name, field_val in user_data.json().items():
        tutor['user:' + field_name] = field_val
    for field_name, field_val in course_data.json().items():
        tutor['course:' + field_name] = field_val

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    del tutor['user:password']

    return tutor

# Details a specific tutor
def detail(request, tutor_id):
    if request.method != "GET":
        return HttpResponseBadRequest()

    json_data = requests.get(API_BASE + 'tutors/{}/?format=json'.format(tutor_id))

    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()

    tutor_data = _tutor_foreign_key_id_to_json(json_data.json())
    tutor_data['num_tutees'] = get_tutor_num_tutees(tutor_id)

    return HttpResponse(json.dumps(tutor_data))

def _tutor_foreign_key_id_to_json(tutor):
    user_data = requests.get(UX_BASE + 'users/{}/'.format(tutor['user']))
    course_data = requests.get(UX_BASE + 'courses/{}/'.format(tutor['course']))

    if (user_data.status_code, course_data.status_code) != (status.HTTP_200_OK,) * 2:
        return "???"

    tutor['user'] = user_data.json()
    tutor['course'] = course_data.json()

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    del tutor['user']['password']

    return tutor

def create(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest()

    # attempt to get a list of all obects from the API, so we can see if the
    # given info already exists in our system
    tutor_list = requests.get(API_BASE + 'tutors/?format=json')

    if tutor_list.status_code != 200:
        return HttpResponseServerError()


    for tutor in tutor_list.json():
        user_matches  = request.POST.get('user') == str(tutor['user'])
        course_matches = request.POST.get('course') == str(tutor['course'])

        if user_matches and course_matches:
            # uh-oh, it already exists in system
            return HttpResponseBadRequest()

    # If it wasn't found in the database already, send a POST request with the needed info.
    new_tutor_data = requests.post(API_BASE + 'tutors/', data=request.POST)

    if new_tutor_data.status_code != 201:
        return HttpResponseServerError()

    #new_tutor_parsed_data = _tutor_foreign_key_id_to_json(new_tutor_data.json())
    new_tutor_parsed_data = _flatten(new_tutor_data.json())
    new_tutor_encoded = json.dumps(new_tutor_parsed_data).encode('utf-8')

    producer.send('new-tutor-listing-topic', new_tutor_encoded)
    #N.B. .content returns bytes instead of text

    return HttpResponse(new_tutor_data.text, status=201)

def get_tutor_num_tutees(tutor_id):
    tutee_data = requests.get(API_BASE + 'tutees/?format=json')

    if tutee_data.status_code != status.HTTP_200_OK:
        return "???"

    #can't return 404 from here :C
    #if tutor_data.status_code != status.HTTP_200_OK:
    #    return HttpResponseNotFound()

    tutee_counter = 0

    for tutee in tutee_data.json():
        if tutee['tutor'] == int(tutor_id):
            tutee_counter += 1

    return tutee_counter


