# Handles Services API urls.
from django.conf.urls import url

from . import views, models, services

urlpatterns = [
    # User API
    url(r'^api/v1/users/create$', services.User.create),
    url(r'^api/v1/users/(?P<user_id>\d+)$', services.User.lookup),

    # Institution API
    url(r'^api/v1/institutions/create$', services.Institution.create),
    url(r'^api/v1/institutions/(?P<inst_id>\d+)$', services.Institution.lookup),
]
