import inject
import json
import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
# from rest_framework import generics
# from django.contrib.auth.models import User
# from django.http import HttpResponse
# from myapp.user.serializers import UserSerializer
# from rest_framework import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth import authenticate
# from rest_framework.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_200_OK
# )

from myapp.serializer.auth_serializer import TokenSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.permission.user_permission import IsAdminUser
logger = logging.getLogger(__name__)


class AuthHandler(TemplateView):
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


# class LoginUser(APIView):
#     usecase = inject.attr(UsecaseInterface)
#     bh = inject.attr(BaseHandler)

#     def get(self, request):
#         context = {"message": "validate success"}
#         return render(request, 'authen/login.html', context)

#     def post(self, request):
#         login_data = request.POST.dict()
#         username = login_data.get("username")
#         password = login_data.get("password")
#         result = self.usecase.get_user(username,password)
#         if username is None or password is None:
#             return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({'error': 'Please fill in correct username and password'}, status=HTTP_404_NOT_FOUND)
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=HTTP_200_OK)
