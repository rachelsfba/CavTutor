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

from CavTutor.user import views as user_views
from CavTutor.institution import views as institution_views
from CavTutor.tutor import views as tutor_views
from CavTutor.tutee import views as tutee_views
from CavTutor.course import views as course_views
from CavTutor import views

urlpatterns = [
    url(r'^institutions/(?P<inst_id>\d+)/?', institution_views.detail, name='institution-detail'),
    url(r'^institutions/?$', institution_views.listings, name='institution-list'),
    url(r'^institution_new/?$', institution_views.institution_new, name='institution-new'),


    url(r'^courses/(?P<course_id>\d+)/?$', course_views.detail, name='course-detail'),
    url(r'^courses/?$', course_views.listings, name='course-list'),

    url(r'^users/(?P<user_id>\d+)/?$', user_views.detail, name='user-detail'),
    url(r'^users/?$', user_views.listings, name='user-list'),

    url(r'^tutors/(?P<tutor_id>\d+)/?$', tutor_views.detail, name='tutor-detail'),
    url(r'^tutors/?$', tutor_views.listings, name='tutor-list'),

    url(r'^tutees/(?P<tutee_id>\d+)/?$', tutee_views.detail, name='tutee-detail'),
    url(r'^tutees/?$', tutee_views.listings, name='tutee-list'),

    url(r'^login/?$', user_views.login, name='user-login'),
    url(r'^logout/?$', user_views.logout, name='user-logout'),
    url(r'^register/?$', user_views.register, name='user-register'),

    url(r'^$|^index/?$', views.index, name='index'),
]
