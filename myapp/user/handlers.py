import inject, json, logging

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from myapp.user.requests import *
from myapp.user.usecases import *
from shared.base_handler import *
from myapp.models.user_serializer import UserSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


logger = logging.getLogger(__name__)

class AuthHandler(APIView):
    usecase = inject.attr(UsecaseInterface)
    bh = inject.attr(BaseHandler)

    def post(self, request):
        response = self.bh.validate(UserRegister, request.POST)
        if response is not None:
            return response
        login_data = request.POST.dict()
        username = login_data.get("username")
        email = login_data.get("email")
        password = login_data.get("password")
        result = self.usecase.create_user(username,email,password)
        if result is None:
            return Response({"messege":"fail"},status=400)
        else:
            serializers = UserSerializer(result)
            return Response(serializers.data,status=200)

    def get(self, request):
        # response = self.bh.validate(UserRegister, request.POST)
    
        context = {"message": "validate success"}
        return render(request, 'authen/register.html', context)
