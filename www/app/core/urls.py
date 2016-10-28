"""ux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from CavTutor import views

urlpatterns = [
    url(r'^institutions/(?P<inst_id>\d+)/?', views.institution_detail, name='institution-detail'),
    url(r'^institutions/?$', views.institution_list, name='institution-list'),

    url(r'^courses/(?P<course_id>\d+)/?$', views.course_detail, name='course-detail'),
    url(r'^courses/?$', views.course_list, name='course-list'),

    url(r'^users/(?P<user_id>\d+)/?$', views.user_detail, name='user-detail'),
    url(r'^users/?$', views.user_list, name='user-list'),

    url(r'^tutors/(?P<tutor_id>\d+)/?$', views.tutor_detail, name='tutor-detail'),
    url(r'^tutors/?$', views.tutor_list, name='tutor-list'),

    url(r'^tutees/(?P<tutee_id>\d+)/?$', views.tutee_detail, name='tutee-detail'),
    url(r'^tutees/?$', views.tutee_list, name='tutee-list'),

    url(r'^login/?$', views.user_login, name='user-login'),
    url(r'^logout/?$', views.user_logout, name='user-logout'),
    url(r'^register/?$', views.user_register, name='user-register'),

    url(r'^$|^index/?$', views.index, name='index'),
]
