from django.urls import include, path
from django.views.generic import TemplateView
from . import views

from rest_auth.registration import urls

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"register", views.SignUpViewSet, base_name="signup")

urlpatterns = []
urlpatterns += router.urls