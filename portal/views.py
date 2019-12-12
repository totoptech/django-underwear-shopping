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