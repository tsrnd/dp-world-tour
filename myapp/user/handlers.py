import inject
import json
import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
from myapp.permission.user_permission import IsAdminUser
# from myapp.models.user_serializer import UserSerializer
# from rest_framework import serializers
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView

from myapp.serializer.auth_serializer import TokenSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

logger = logging.getLogger(__name__)

class AuthHandler(GenericAPIView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    # def post(self, request):
    #     response = self.bh.validate(UserRegister, request.POST)
    #     if response is not None:
    #         return response
    #     context = {"message": "validate success"}
    #     return render(request, 'base.html', context)

    # def get(self, request):
    #     # response = self.bh.validate(UserRegister, request.POST)
    #     context = {"message": "validate success"}
    #     return render(request, 'authen/register.html', context)


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
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegisterAPIView(GenericAPIView):
    usecase = inject.attr(UsecaseInterface)
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
        result = self.usecase.create_user(username,email,password)
        if result is None:
            return Response({"messege":"fail"},status=400)
        # user = serializer.user
        user = authenticate(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data=TokenSerializer(token).data,status=HTTP_200_OK)
