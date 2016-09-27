# Handles Services API urls.
from django.conf.urls import url

from . import views, models, services

urlpatterns = [
    # User API
    url(r'^api/v1/users/create$', services.User.create),
    url(r'^api/v1/users/(?P<id>\d+)$', services.User.lookup),
    url(r'^api/v1/users/delete/(?P<id>\d+)$', services.User.delete),

    # Institution API
    url(r'^api/v1/institutions/create$', services.Institution.create),
    url(r'^api/v1/institutions/(?P<id>\d+)$', services.Institution.lookup),
#    url(r'^api/v1/institutions/delete/(?P<id>\d+)$', services.Institution.delete),
]
