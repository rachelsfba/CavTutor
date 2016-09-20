from django.conf.urls import url

from . import views, models, services

urlpatterns = [
    url(r'^api/v1/users/create$', services.create_user),
    url(r'^api/v1/users/(\d+)$', services.lookup_user)
    #url(r'^api/v1/(?P<model>[a-z]+)/(?P<action>[a-z0-9]+)$', views.api_handler),

]
