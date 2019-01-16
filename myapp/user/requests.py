from django.core import validators
from rest_framework import serializers

class UserRegister(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100,validators=[validators.validate_email])
    password = serializers.CharField(max_length=100)
