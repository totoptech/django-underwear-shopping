from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, db_index=True)
    brasize = models.CharField(max_length=255, null=True, blank=True)
    pantysize = models.CharField(max_length=255, null=True, blank=True)
    bottomsize = models.CharField(max_length=255, null=True, blank=True)
    topsize = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField('active', default=True)

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    REQUIRED_FIELDS = ['firstname', 'lastname']
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    @property
    def is_staff(self):
        return self.is_superuser

class PortfolioLike(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    uniq_id = models.CharField(max_length=255, null=True, blank=True)
    lol = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Portfolio Like'

class Gift(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    uniq_id = models.CharField(max_length=255, null=True, blank=True)
    gift = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = "Gift"

class Friend(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    friend = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Friend'

class ProductRank(models.Model):
    uniq_id = models.CharField(max_length=255, null=True, blank=True)
    rank = models.IntegerField(null=True)
    
    class Meta:
        verbose_name_plural = 'Ranking'