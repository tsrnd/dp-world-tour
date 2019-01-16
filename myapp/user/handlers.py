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
from shared.token import TokenBase
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


class TokenView(APIView):
    token_base = inject.attr(TokenBase)

    def post(self, request, format=None):
        token = self.token_base.generate_token(
            request.data)

        content = {
            'token': token
        }
        return Response(content)
