from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.six import text_type


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}


class AuthenticateSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(AuthenticateSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        super(AuthenticateSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)
        data = {}
        data['token'] = text_type(refresh.access_token)

        return data


class AuthenticateSerializerView(TokenObtainPairView):
    serializer_class = AuthenticateSerializer
