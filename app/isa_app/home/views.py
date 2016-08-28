from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from home.models import User

def get_user_records(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    our_user, is_new = User.objects.get_or_create(ip_address=ipaddress)
    our_user.save()

    return our_user

def index(request):

    cur_user = get_user_records(request)
    cur_user.times_visited += 1
    cur_user.save()

    context = {
        'body_text': 'Hello, world. This is the main page of the Internet Scale Appliations Project No. 1. You have visited this page {} times.'.format(cur_user.times_visited),
    }
    return render(request, 'home/index.html', context)
