from django.shortcuts import render
from django.http.response import HttpResponse

from urllib.request import urlopen
from urllib.error import HTTPError

#import requests
import json

API_BASE = 'http://api:8000/'
"""
    Institutions
"""
# List of all institution objects
def institution_list(request):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'institutions/?format=json').read()

    return HttpResponse(json_data)

# Details a specific institution object
def institution_detail(request, inst_id):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).read().decode('utf-8')
    data = json.loads(json_data)

    # add two additional boolean fields to what the API gave us
    data['num_courses'] = get_institution_num_courses(int(inst_id))

    return HttpResponse(json.dumps(data))


def get_institution_name(inst_id):
    json_data = urlopen(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).read().decode('utf-8')
    data = json.loads(json_data)

    return data['name']

def get_institution_num_courses(inst_id):
    courses_json = urlopen(API_BASE + 'courses/?format=json').read().decode('utf-8')
    courses_data = json.loads(courses_json)

    inst_counter = 0

    for course in courses_data:
        if course['institution'] == int(inst_id):
            inst_counter += 1

    return inst_counter

"""
    Users
"""
# List of all user objects
def user_list(request):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'users/?format=json').read()

    return HttpResponse(json_data)

# Details a specific user object
def user_detail(request, user_id):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'users/{}/?format=json'.format(user_id)).read().decode('utf-8')
    data = json.loads(json_data)

    # add two additional boolean fields to what the API gave us
    data['is_tutor'] = user_is_tutor(int(user_id))
    data['is_tutee'] = user_is_tutee(int(user_id))

    return HttpResponse(json.dumps(data))

def user_is_tutee(user_id):
    tutee_json = urlopen(API_BASE + 'tutees/?format=json').read().decode('utf-8')
    tutee_data = json.loads(tutee_json)

    for record in tutee_data:
        if record['user'] == user_id:
            return True

    return False


def user_is_tutor(user_id):
    tutor_json = urlopen(API_BASE + 'tutors/?format=json').read().decode('utf-8')
    tutor_data = json.loads(tutor_json)

    for record in tutor_data:
        if record['user'] == user_id:
            return True

    return False


"""
    Tutors
"""
# List of all tutors
def tutor_list(request):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'tutors/?format=json').read()

    return HttpResponse(json_data)

# Details a specific tutor
def tutor_detail(request, tutor_id):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'tutors/{}/?format=json'.format(tutor_id)).read()
    return HttpResponse(json_data)

"""
    Tutees
"""
# List of all tutees
def tutee_list(request):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'tutees/?format=json').read()

    return HttpResponse(json_data)

# Details a specific tutee
def tutee_detail(request, tutee_id):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'tutees/{}/?format=json'.format(tutee_id)).read()
    return HttpResponse(json_data)

"""
    Courses
"""
# List of all courses
def course_list(request):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'courses/?format=json').read()

    return HttpResponse(json_data)

# Details a specific course
def course_detail(request, course_id):
    if request.method != "GET":
        return HttpResponse(status=400)

    json_data = urlopen(API_BASE + 'courses/{}/?format=json'.format(course_id)).read().decode('utf-8')
    data = json.loads(json_data)

    data['num_tutors'] = get_course_num_tutors(course_id)
    data['institution_name'] = get_institution_name(data['institution'])

    return HttpResponse(json.dumps(data))

def get_course_num_tutors(course_id):
    tutors_json = urlopen(API_BASE + 'tutors/?format=json').read().decode('utf-8')
    tutors_data = json.loads(tutors_json)

    tutor_counter = 0

    for tutor in tutors_data:
        if tutor['course'] == int(course_id):
            tutor_counter += 1

    return tutor_counter
