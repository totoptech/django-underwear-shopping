import logging
import json
import traceback
import os, re
import pandas as pd

from django.conf import settings
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny, IsAdminUser)
from rest_framework.viewsets import ModelViewSet
from portal.serializers import UnwravelSignupSerializer
from rest_framework.authtoken.models import Token
import datetime
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('mcq.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.debug("portal/views.py: __name__=%s" % __name__)

# Create your views here.
#================== when first page is loaded ==============================
def portal_index(request):
    if request.user.is_authenticated:
        return redirect('portal_user')
    
    return redirect('portal_signin')

#================== SIGN IN ==============================
def portal_signin(request):
    logger.info(request.user.is_authenticated)
    if request.user.is_authenticated: # to avoid go to login screen again without logout.
        return redirect('portal_index')

    strMessage = ""
    if request.method=='POST':

        username = request.POST['email']
        password = request.POST['password']
        if __login(request, username,password):
            return redirect('portal_user')
        else:
            strMessage = "Username or password is invalid!"
    response = render(request,"signin.html",{ "message": strMessage} )
    return response