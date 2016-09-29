# Handles Services API urls.
from django.conf.urls import url

urlpatterns = [
    # User API
    url(r'^api/v1/users/create$', 'CavTutor.services.users.User.create'),
    url(r'^api/v1/users/(?P<id>\d+)$', 'CavTutor.services.users.User.lookup'),
    url(r'^api/v1/users/delete/(?P<id>\d+)$', 'CavTutor.services.users.User.delete'),

    # Institution API
    url(r'^api/v1/institutions/create$', 'CavTutor.services.institutions.User.create'),
    url(r'^api/v1/institutions/(?P<id>\d+)$', 'CavTutor.services.institutions.User.lookup'),
#    url(r'^api/v1/institutions/delete/(?P<id>\d+)$', 'services.institutions.delete'),
]
