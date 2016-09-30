# Handles API urls.
from django.conf.urls import url, include
from django.conf import settings

BASE_PATH = r'^api/' + settings.API_VERSION

urlpatterns = [
    url(BASE_PATH + r'/.*$', include('CavTutor.api.urls')),
]
