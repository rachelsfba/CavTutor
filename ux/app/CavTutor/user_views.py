import json, requests

from core.settings import API_BASE, UX_BASE

from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

from rest_framework import status

HTTP_ERROR_500 = json.dumps(dict(detail="HTTP 500 Error: Internal Service Error"))
HTTP_ERROR_400 = json.dumps(dict(detail="HTTP 400 Error: Bad Request"))
HTTP_ERROR_404 = json.dumps(dict(detail="HTTP 404 Error: File Not Found"))

# List of all user objects
def user_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'users/?format=json').read()
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    return HttpResponse(json_data)

# Details a specific user object
def user_detail(request, user_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    try:
        json_data = urlopen(API_BASE + 'users/{}/?format=json'.format(user_id)).read().decode('utf-8')
    except HTTPError as e:
        return HttpResponseNotFound(HTTP_ERROR_404)

    data = json.loads(json_data)

    # add two additional boolean fields to what the API gave us
    data['is_tutor'] = _user_is_tutor(int(user_id))
    data['is_tutee'] = _user_is_tutee(int(user_id))

    return HttpResponse(json.dumps(data))

def user_login(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest(HTTP_ERROR_400)
    
    # attempt to get a list of all users from the API, so we can validate
    # against the username and password in the POST data
    try:
        json_data = urlopen(API_BASE + 'users/?format=json').read().decode('utf-8')
    except HTTPError as e:
        # If users listing didn't work sfor some reason, 
        return HttpResponseNotFound(HTTP_ERROR_404)

    data = json.loads(json_data)

    # we have to iterate over all the users in the entire listing. need to find
    # a more RESTful and efficient way
    for user in data:
        # for every user in the data, check if their usernamd and password
        # match what is in the POST data
        if request.POST['username'] == user['username'] and \
            check_password(request.POST['password'], user['password']):
           
            # create a dictionary with the two fields the API will need to
            # create a new cookie
            response_context = {
                    'user': user['id'],
                    'token': _make_new_auth_cookie(),
                   }

            # encode the data we need to send to the API
            encoded_data = urlencode(response_context).encode('utf-8')

            # try to post encoded_data to Authenticator api
            try:
                api_auth_data = urlopen(API_BASE + 'authenticators/', data=encoded_data).read().decode('utf-8')
            except HTTPError as e:
                return HttpResponseServerError(e)
            
            #return cookie to front end
            return HttpResponse(api_auth_data)

    return HttpResponseNotFound(HTTP_ERROR_404)

def _make_new_auth_cookie():

    authenticator = hmac.new(
            key = settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256').hexdigest()

    return authenticator

def _user_is_tutee(user_id):
    tutee_json = urlopen(API_BASE + 'tutees/?format=json').read().decode('utf-8')
    tutee_data = json.loads(tutee_json)

    for record in tutee_data:
        if record['user'] == user_id:
            return True

    return False


def _user_is_tutor(user_id):
    tutor_json = urlopen(API_BASE + 'tutors/?format=json').read().decode('utf-8')
    tutor_data = json.loads(tutor_json)

    for record in tutor_data:
        if record['user'] == user_id:
            return True

    return False










# List of all institution objects
def listings(request):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)
    
    data = requests.get(API_BASE + 'institutions/?format=json')

    if data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound(HTTP_ERROR_404)

    return HttpResponse(data.text)


# Details a specific institution object
def detail(request, inst_id):
    if request.method != "GET":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    json_data = requests.get(API_BASE + 'institutions/{}/?format=json'.format(inst_id))
    
    if json_data.status_code != status.HTTP_200_OK:
        return HttpResponseNotFound(HTTP_ERROR_404)

    data = json_data.json()
    data['num_courses'] = get_institution_num_courses(int(inst_id))

    return HttpResponse(json.dumps(data))


def get_institution_name(inst_id):
    data = requests.get(API_BASE + 'institutions/{}/?format=json'.format(inst_id)).json()

    return data['name']

def get_institution_num_courses(inst_id):

    courses_data = requests.get(API_BASE + 'courses/?format=json').json()

    count = 0

    for course in courses_data:
        if course['institution'] == int(inst_id):
            count += 1

    return count

def create(request):
    # web frontend must send a POST request to ux
    if request.method != "POST":
        return HttpResponseBadRequest(HTTP_ERROR_400)

    # attempt to get a list of all obects from the API, so we can see if the
    # given info already exists in our system
    inst_list = requests.get(API_BASE + 'institutions/?format=json')

    if inst_list.status_code != 200:
        # If users listing didn't work for some reason, 
        return HttpResponseServerError(HTTP_ERROR_500)
    
    # we have to iterate over all the institutions in the entire listing. need to find
    # a more RESTful and efficient way
    for inst in inst_list.json():
        # for every institution, match the POSTed name with this record's name
        # to check for duplicates
        if request.POST.get('name') == inst['name']:
            # uh-oh, it already exists in system
            return HttpResponseBadRequest(HTTP_ERROR_400)
    
    # If it wasn't found in the database already, send a POST request with the needed info.
    new_inst_data = requests.post(API_BASE + 'institutions/', data=request.POST)

    if new_inst_data.status_code != 201:
        return HttpResponseServerError(HTTP_ERROR_500)

    return HttpResponse(new_inst_data.text, status=201)


