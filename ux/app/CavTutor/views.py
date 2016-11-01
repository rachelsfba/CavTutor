"""
    MODULE:
    CavTutor.views
    
    DESCRIPTION:
    Handles general views for the UX layer.
"""

""" We need these libraries to parse the API layer's JSON responses into Python
    data structures, as well as to update the database through sending data back
    to the API layer. """
import requests, json 

""" These libraries are needed for cookie token generation. """
import os, hmac

""" We need to get the API_BASE prefix from the settings file so that we can
    access the API information. """
from core.settings import API_BASE

"""  We utilize some common Django idioms, so fetch those implementations. """
from django.shortcuts import render
from django.http.response import *
from django.contrib.auth.hashers import check_password, make_password

""" rest_framework.status has a list HTTP status codes, which keeps us from
    having to write our own. """
from rest_framework import status

# There's nothing here for now!
