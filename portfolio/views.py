import pandas as pd
import numpy as np
from io import StringIO

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from accounts.models import Account
from django.conf import settings
# from apps.portfolio.models import Portfolio
# from apps.portfolio.serializers import (CreatePortfolioSerializer,
#                                         PortfolioDetailSerializer,
#                                         PortfolioSerializer)

from accounts.models import Account
from accounts.serializers import AccountSerializer
from portfolio.serializers import PortfolioLikeSerializer
from accounts.models import PortfolioLike
from accounts.models import Gift
from accounts.models import Friend
from accounts.models import ProductRank
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


class PortfolioListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, *args, **kwargs):
        print("user: ", self.request.user)
        account = Account.objects.get(email=self.request.user)

        path = settings.BASE_DIR + '/static/victoria_secret.json'
        json_data = open(path)
        json_portfolios = json.load(json_data)
        topsize = account.topsize
        bottomsize = account.bottomsize
        brasize = account.brasize
        pantysize = account.pantysize
        json_result = []
        for portfolio in json_portfolios:
            
            product_category = portfolio['product_category']
            available_size = portfolio['available_size']
            uniq_id = portfolio['uniq_id']
            
            portfoliolike = PortfolioLike.objects.filter(account=account, uniq_id = uniq_id)
            if portfoliolike:
                portfolio['lol'] = portfoliolike[0].lol
            else:
                portfolio['lol'] = 0
            productrank = ProductRank.objects.filter(uniq_id = uniq_id)

            # gift = Gift.objects.filter(account=account, uniq_id = uniq_id)
            # if len(gift) == 0:
            if product_category == "Panties":
                if pantysize in available_size:
                    json_result.append(portfolio)
            if product_category == "Lingerie":
                if topsize in available_size:
                    json_result.append(portfolio)
            if product_category == "Bras":
                if brasize in available_size:
                    json_result.append(portfolio)
            # if product_category == "Panties":
            #     if pantysize in available_size:
            #         json_result.append(portfolio)

        return Response(
            data=json_result,
            status=status.HTTP_200_OK,
            )


class BrideListAPIView(RetrieveAPIView):

    def post(self, request, *args, **kwargs):

        account = Account.objects.get(email=request.data['email'])
        print(account.id);
        path = settings.BASE_DIR + '/static/victoria_secret.json'
        json_data = open(path)
        json_portfolios = json.load(json_data)
        json_result = []
        for portfolio in json_portfolios:
            uniq_id = portfolio['uniq_id']
            portfoliolike = PortfolioLike.objects.filter(account_id=account.id, uniq_id = uniq_id)

            if portfoliolike:
                if(portfoliolike[0].lol >= 1):
                    portfolio['lol'] = portfoliolike[0].lol
                    json_result.append(portfolio)
        return Response( data=json_result,
                        status=status.HTTP_200_OK)

class EditProfileAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        account = Account.objects.get(email=self.request.user)
        account.firstname = request.data['firstname']
        account.lastname = request.data['lastname']
        account.brasize = request.data['brasize']
        account.pantysize = request.data['pantysize']
        account.bottomsize = request.data['bottomsize']
        account.topsize = request.data['topsize']
        account.save()
        return Response(
            {'status': "OK"},
            status=status.HTTP_200_OK)

class PortfolioListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    print("I am here")


def portfolioList(request):
	user = request.user
	try:
		print("account", user.email)
	except:
		pass

	return HttpResponse("OK")

class PortfolioLikeAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PortfolioLikeSerializer

    def create(self, request, *args, **kwargs):
        uniq_id = request.data['uniq_id']
        lolstate = request.data['lol']
        portfoliolike = PortfolioLike.objects.get_or_create(
            account=self.request.user, 
            uniq_id = uniq_id)
        if portfoliolike[0].lol == 1:
            update_rank(uniq_id,-1,0,0)
        if portfoliolike[0].lol == 2:
            update_rank(uniq_id,0,-1,0)
        if lolstate == 1:
            update_rank(uniq_id,1,0,0)
        if lolstate == 2:
            update_rank(uniq_id,0,1,0)
        print(lolstate, portfoliolike[0].lol)
        portfoliolike[0].lol = lolstate
        portfoliolike[0].save()
        return Response(
            {'status': "OK"},
            status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        portfoliolike = PortfolioLike.objects.create(
            account=self.request.user, 
            uniq_id = serializer.data['uniq_id'],
            lol = serializer.data['lol'])
        return portfoliolike

    def get_queryset(self):
        return PortfolioLike.objects \
            .filter(account=self.request.user)

class GiftListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, *args, **kwargs):
        account = Account.objects.get(email=self.request.user)
        path = settings.BASE_DIR + '/static/victoria_secret.json'
        json_data = open(path)
        json_portfolios = json.load(json_data)
        json_result = []
        for portfolio in json_portfolios:
            uniq_id = portfolio['uniq_id']
            portfoliolike = PortfolioLike.objects.filter(account=account, uniq_id = uniq_id)
            if portfoliolike:
                if portfoliolike[0].lol == 2:
                    portfolio['lol'] = 2
                    json_result.append(portfolio)
        return Response( data=json_result,
                        status=status.HTTP_200_OK)


class AddGiftAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        uniq_id = request.data['uniq_id']
        gift = Gift.objects.get_or_create(
            account=self.request.user,
            uniq_id = uniq_id)
        update_rank(uniq_id,0,0,1)
        return Response(
            {'status':'OK'},
            status=status.HTTP_201_CREATED)

class RemoveGiftAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        uniq_id = request.data['uniq_id']
        gift = Gift.objects.filter(
            account=self.request.user,
            uniq_id = uniq_id).delete()

        return Response(
            {'status':'OK'},
            status=status.HTTP_201_CREATED)

class AddFriendAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        friend = Friend.objects.get_or_create(
            account=self.request.user,
            friend=request.data['email'])
        friend[0].friend = request.data['email']
        friend[0].save()
        email_list = []
        email_list.append(request.data['email'])
        account = Account.objects.get(email=self.request.user)
        send_mail('Congratulation',
            '',
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            html_message =  account.email + " send invitation to you on unwravel.com. You can see his gifts with your privacy",
            fail_silently=False
            )
        return Response(
            {'status':'OK'},
            status=status.HTTP_200_OK)

class FriendListAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        print(self.request.user)
        friends = Friend.objects.filter(
            account=self.request.user)
        json = []
        for friend in friends:
            json.append(friend.friend)

        return Response(
            data=json,
            status=status.HTTP_200_OK)
class DeleteFriendAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        friend = Friend.objects.get(
            account=self.request.user,
            friend=request.data['email']).delete()
        
        return Response(
            {'status':'OK'},
            status=status.HTTP_200_OK)   


class IsFriendAPIView(RetrieveAPIView):

    def post(self, request, *args, **kwargs):
        myEmail = request.data['myEmail']
        brideEmail = request.data['brideEmail']
        print(myEmail,brideEmail)
        account = Account.objects.filter(email=brideEmail)
        if account:
            friend = Friend.objects.filter(
                account_id=account[0].id,
                friend=myEmail)
            print(friend)
            if friend:
                return Response(
                    data=serializers.serialize("json",account),
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'status':'Your email is not valid'},
                    status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {'status':'Bride Email is not valid'},
                status=status.HTTP_202_ACCEPTED)

def test_send_message(request):
    send_mail('Friend Message',
            '',
            settings.DEFAULT_FROM_EMAIL,
            ['nicknovak88@hotmail.com'],
            html_message = "Added Friend",
            fail_silently=False
            )
    return HttpResponse("Ok")

def initialize_rankinformation(request):
    path = settings.BASE_DIR + '/static/victoria_secret.json'
    json_data = open(path)
    json_portfolios = json.load(json_data)
    json_result = []
    for portfolio in json_portfolios:
        uniq_id = portfolio['uniq_id']
        product_rank = ProductRank.objects.get_or_create(uniq_id = uniq_id)
        product_rank[0].rank = 0
        product_rank[0].save()
    return HttpResponse("Ok")


def update_rank(uniq_id, like, love, gift):
    product = ProductRank.objects.get(uniq_id = uniq_id)
    rank = product.rank + love * settings.LOVE_WEIGHT + like * settings.LIKE_WEIGHT + gift * settings.GIFT_WEIGHT
    product.rank = rank
    product.save()
    return HttpResponse("Ok")
