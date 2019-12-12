from django.contrib import admin
from django.urls import path
from django.conf.urls import  include, url
from portal import views as portal_views
from django.conf import settings
from django.template import RequestContext
from django import template
from django.template import Context
from rest_framework.schemas import get_schema_view
from .views import PortfolioListAPIView
from .views import PortfolioLikeAPIView
from .views import AddGiftAPIView
from .views import GiftListAPIView
from .views import AddFriendAPIView
from .views import FriendListAPIView
from .views import IsFriendAPIView
from .views import BrideListAPIView
from .views import EditProfileAPIView
from .views import DeleteFriendAPIView
from .views import RemoveGiftAPIView
from portfolio import views as portfolio_views

urlpatterns = [
    path(
        '',
        PortfolioListAPIView.as_view(),
        name='portfolio-list',
    ),
    path(
        'changeLOL/',
        PortfolioLikeAPIView.as_view(),
        name='portfolio-like',
    ),
    path(
    	'addGift/',
    	AddGiftAPIView.as_view(),
    	name='add-gift'
    ),
    path(
    	'removeGift/',
    	RemoveGiftAPIView.as_view(),
    	name='remove-gift'
    ),
    path(
    	'getgift/',
    	GiftListAPIView.as_view(),
    	name='gift-list'
    ),
    path(
    	'addFriend/',
    	AddFriendAPIView.as_view(),
    	name='add-friend'

   	),
   	path(
   		'getFriends/',
   		FriendListAPIView.as_view(),
   		name='friend-list'
   	),
   	path(
   		'isFriend/',
   		IsFriendAPIView.as_view(),
   		name='is-friend'
   	),
   	path(
   		'getBride/',
   		BrideListAPIView.as_view(),
   		name='bride-list'
   	),
   	path(
   		'editProfile/',
   		EditProfileAPIView.as_view(),
   		name='edit-profile'
   	),
   	path(
   		'deleteFriend/',
   		DeleteFriendAPIView.as_view(),
   		name='delete-friend'
   	),
    url(r'^test_send_message/', portfolio_views.test_send_message, name='test_send_message'),
    url(r'^initialize_rank/',portfolio_views.initialize_rankinformation, name='initialize_rankinformation')
]
