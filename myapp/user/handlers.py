import inject
import json
import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
from myapp.serializer.auth_serializer import UserLoginSerializer, TokenSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.permission.user_permission import IsAdminUser
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


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserInfoAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
