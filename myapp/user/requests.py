from django.core import validators
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=100,required=True, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    email = serializers.EmailField(max_length=100, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(max_length=100,required=True)
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)
        self.user = None

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get(
            "username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(
                    self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials'])
