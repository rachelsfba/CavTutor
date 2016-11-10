import requests, json

API_VERSION = 'v2'
API_BASE = 'http://api:8000/api/' + API_VERSION + "/"
UX_BASE = 'http://localhost:8000/'
ELASTIC_SEARCH_NUM_RESULTS = 25

from django.shortcuts import render
from django.http.response import *
from rest_framework import status
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='kafka:9092')


def _flatten(tutor):
    user_data = requests.get(API_BASE + 'users/{}/'.format(tutor['user']))
    course_data = requests.get(API_BASE + 'courses/{}/'.format(tutor['course']))

    for field_name, field_val in user_data.json().items():
        tutor['user:' + field_name] = field_val
    for field_name, field_val in course_data.json().items():
        tutor['course:' + field_name] = field_val

    # don't even THINK about giving the web layer a password without it
    # explicitly requiring it!~
    del tutor['user:password']

    return tutor



# Load all fiztures into the producer 
def load_fixtures():
    tutor_data = requests.get(API_BASE + 'tutors/?format=json')

    if tutor_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound()
    for tutor in tutor_data.json():
        print(tutor)
        new_tutor_parsed_data = _flatten(tutor)
        new_tutor_encoded = json.dumps(new_tutor_parsed_data).encode('utf-8')
        producer.send('new-tutor-listing-topic', new_tutor_encoded)

load_fixtures()
