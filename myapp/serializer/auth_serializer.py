from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.six import text_type
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username', 'date_joined',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("token", )
