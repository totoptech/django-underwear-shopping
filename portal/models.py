# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

class UnwravelUserManager(BaseUserManager):
    """
    custom user manager for leasing user 
    this user manager is responsible for all 
    CRUD operation over custom user models  
    """

    def create_user(self, email=None, password=None):
        if not email or email is None:
            raise ValidationError("User must have email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UnwravelUser(AbstractBaseUser):
    username = None
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    brasize = models.CharField(max_length=255, null=True, blank=True)
    pantysize = models.CharField(max_length=255, null=True, blank=True)
    bottomsize = models.CharField(max_length=255, null=True, blank=True)
    topsize = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UnwravelUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def display_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.email

