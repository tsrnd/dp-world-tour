import inject
import json
import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from myapp.user.requests import *
from shared.base_handler import *
from myapp.permission.user_permission import IsAdminUser
from myapp.serializer.auth_serializer import TokenSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class AuthHandler(GenericAPIView):
    bh = inject.attr(BaseHandler)
    
    
class UserLoginAPIView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )


class UserInfoAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegisterAPIView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        username = serializer.data.get("username")
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        if user is None:
            return Response({"messege":"fail"},status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data=TokenSerializer(token).data,status=status.HTTP_200_OK)
