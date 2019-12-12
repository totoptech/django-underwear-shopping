# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        CreateOnlyDefault, CurrentUserDefault)
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import UnwravelUser

class UnwravelSignupSerializer(ModelSerializer):
    token = SerializerMethodField()

    def get_token(self, instance):
        return Token.objects.get(user=instance).key

    class Meta:
        model =  UnwravelUser
        exclude = ('last_login',
                   'is_active',
                   'is_staff',
                   'is_admin',
                   'date_joined')
