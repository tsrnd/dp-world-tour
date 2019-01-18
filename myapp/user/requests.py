from django.core import validators
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

class UserRegister(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100,validators=[validators.validate_email])
    password = serializers.CharField(max_length=100)


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
