from django.shortcuts import render
from django.http import JsonResponse

from .models import *

# Create your views here.
def api_handler(request, model, action):

    dict_info = {}

    # call appropriate handler here
    if model == "user":
        dict_info = user_api_handler(request, action)
    elif model == "tutor":
        dict_info = tutor_api_handler(request, action)
    elif model == "tutee":
        dict_info = tutee_api_handler(request, action)
    elif model == "course":
        dict_info = course_api_handler(request, action)
    elif model == "institution":
        dict_info = institution_api_handler(request, action)

    return JsonResponse({'ok': False,
        'result' : dict_info})

def user_api_handler(request, action):
    if action == "create":
        user = User(f_name=request.POST['f_name'],
                l_name=request.POST['l_name'],
                email=request.POST['email'],
                username=request.POST['username'],
                password=request.POST['password'],
                date_joined=request.POST['date_joined'])
        user.save()
    else:
        try:
            user = User.objects.get(id=action)
        except User.DoesNotExist:
            user = None

    return {} if user == None else user.to_dict()


def tutor_api_bandler(request, action):
    return

def tutee_api_bandler(request, action):
    return

def institution_api_bandler(request, action):
    return

def course_api_bandler(request, action):
    return
