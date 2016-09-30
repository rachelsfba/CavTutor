# Handles Services API urls.
from django.conf.urls import url
from django.conf import settings

urlpatterns = [

    BASE_PATH = r'^api/' + settings.API_VERSION

    # User API
    url(BASE_PATH + r'/users/create$', 'users.User.create'),
    url(BASE_PATH + r'/users/(?P<id>\d+)$', 'users.User.lookup'),
    url(BASE_PATH + r'/users/delete/(?P<id>\d+)$', 'users.User.delete'),

    # Institution API
    url(BASE_PATH + r'/institutions/create$', 'institutions.Institution.create'),
    url(BASE_PATH + r'/institutions/(?P<id>\d+)$', 'institutions.Institution.lookup'),

    #    url(r'^api/v1/institutions/delete/(?P<id>\d+)$', 'services.institutions.delete'),
]
