# Handles Services API urls.
from django.conf.urls import url

from . import views

urlpatterns = [
    # User API
    url(r'users/create$', views.User.create),
    url(r'users/(?P<id>\d+)$', views.User.lookup),
    url(r'users/delete/(?P<id>\d+)$', views.User.delete),
    url(r'users/update/(?P<id>\d+)$', views.User.update),

    # Institution API
    url(r'institutions/create$', views.Institution.create),
    url(r'institutions/(?P<id>\d+)$', views.Institution.lookup),
    url(r'institutions/delete/(?P<id>\d+)$', views.Institution.delete),
    url(r'institutions/update/(?P<id>\d+)$', views.Institution.update),

]
