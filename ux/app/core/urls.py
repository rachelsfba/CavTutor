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

from CavTutor import views

from CavTutor.institution import views as institution_views
from CavTutor.course import views as course_views
from CavTutor.user import views as user_views
from CavTutor.tutor import views as tutor_views
from CavTutor.tutee import views as tutee_views

from CavTutor.authentication import views as auth_logic

urlpatterns = [
    url(r'^institutions/(?P<inst_id>\d+)/?$', institution_views.detail, name='institution-detail'),
    url(r'^institutions/create/?$', institution_views.create, name='institution-create'),
    url(r'^institutions/?$', institution_views.listings, name='institution-listings'),

    url(r'^courses/(?P<course_id>\d+)/?$', course_views.detail, name='course-detail'),
    url(r'^courses/?$', course_views.listings, name='course-listings'),

    url(r'^tutors/(?P<tutor_id>\d+)/?$', tutor_views.detail, name='tutor-detail'),
    url(r'^tutors/create/?$', tutor_views.create, name='tutor-create'),
    url(r'^tutors/?$', tutor_views.listings, name='tutor-listings'),

    url(r'^tutees/(?P<tutee_id>\d+)/?$', tutee_views.detail, name='tutee-detail'),
    url(r'^tutees/?$', tutee_views.listings, name='tutee-listings'),

    url(r'^users/(?P<user_id>\d+)/?$', user_views.detail, name='user-detail'),
    url(r'^users/(?P<user_id>\d+)/teaching/?$', user_views.tutor_listings, name='user-tutor-listing'),
    url(r'^users/(?P<user_id>\d+)/learning/?$', user_views.tutee_listings, name='user-tutee-listing'),
    url(r'^users/?$', user_views.listings, name='user-listings'),
    
    url(r'^login/?$', auth_logic.login, name='login'),
    url(r'^register/?$', auth_logic.register, name='register'),
    url(r'^logout/?$', auth_logic.logout, name='register'),
    url(r'^validate/?$', auth_logic.validate_user_cookie, name='validate-cookie'),
]
