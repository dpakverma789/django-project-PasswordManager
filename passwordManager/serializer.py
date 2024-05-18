from rest_framework import serializers
from .models import Credentials


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = ('website', 'username', 'password', 'login_user')
