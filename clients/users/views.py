from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import requests
import json


def register(request):
    return render(request, 'authen/register.html', None)


def create_user(request):
    r = requests.post('http://localhost:8000/api/user/register', data={
        'email': 'test',
        'user_name': 'test',
        'password': 'test',
    })
    response = r.json()
    print(response["message"])
    return render(request, 'authen/login.html', None)


permission_classes = (IsAuthenticated,)


def login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        result = requests.post('http://localhost:8000/api/user/login', data={
            'username': username,
            'password': password,
        })
        status_code = result.status_code
        response = result.json()
        if status_code == HTTP_200_OK:
            return redirect('home')
        else:
            return render(request, 'authen/login.html')
    else:
        return render(request, 'authen/login.html')

def home(request):
    return render(request, 'home/index.html')