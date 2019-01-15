import inject
import json
import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from myapp.serializer.auth_serializer import UserSerializer
from rest_framework.views import APIView
from myapp.permissions.auth_permissions import IsAdminUser

logger = logging.getLogger(__name__)


class AuthHandler(TemplateView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def post(self, request):
        response = self.bh.validate(UserRegister, request.POST)
        if response is not None:
            return response
        context = {"message": "validate success"}
        return render(request, 'base.html', context)

    def get(self, request):
        # response = self.bh.validate(UserRegister, request.POST)
        context = {"message": "validate success"}
        return render(request, 'authen/register.html', context)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):

     # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminView(APIView):
    permission_classes = (IsAuthenticated & IsAdminUser,)

    def get(self, request, format=None):
        content = {
            'message': "Admin View"
        }
        return Response(content)
