from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from accounts.models import Account


class RegisterAccountSerializer(RegisterSerializer):
    
    firstname = serializers.CharField(
        required=True,
        label="First name"
    )
    lastname = serializers.CharField(
        required=True,
        label="Last name"
    )
    brasize = serializers.CharField(
        required=True,
        label="Bra size"
    )
    pantysize = serializers.CharField(
        required=True,
        label="Panty size"
    )
    bottomsize = serializers.CharField(
        required=True,
        label="Bottom size"
    )
    topsize = serializers.CharField(
        required=True,
        label="Top size"
    )

    def custom_signup(self, request, user):
        
        user.firstname = self.validated_data.get('firstname')
        user.lastname = self.validated_data.get('lastname')
        user.brasize = self.validated_data.get('brasize')
        user.pantysize = self.validated_data.get('pantysize')
        user.bottomsize = self.validated_data.get('bottomsize')
        user.topsize = self.validated_data.get('topsize')
        user.save()


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('firstname', 'lastname', 'brasize', 'pantysize', 'bottomsize', 'topsize')
