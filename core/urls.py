
from django.contrib import admin
from django.urls import path
from django.conf.urls import  include, url
from portal import views as portal_views
from django.conf import settings
from django.template import RequestContext
from django import template
from django.template import Context
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
]

# portal
urlpatterns += [
    path('api/', get_schema_view()),
    url(r'^signin/$', portal_views.portal_signin, name='portal_signin'),
    url(r'^$', portal_views.portal_index, name='portal_index'),
    url(r'^signout/$', portal_views.portal_signout, name='portal_signout'),
    url(r'^api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/portfolios/', include('portfolio.urls')),
    # url(r'^search/$', portal_views.portal_search, name='portal_search'),
]
