from django.conf.urls import url

from . import views, models, services

urlpatterns = [
    url(r'^api/v1/users/create$', services.User.create),
    url(r'^api/v1/users/(?P<user_id>\d+)$', services.User.lookup)
]
