from django.shortcuts import render
import requests, json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib import messages



def register(request):
    if request.POST:
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        if password == repassword:
            r = requests.post('http://localhost:8000/api/user/register', data={
                'email': email,
                'username': username,
                'password': password,
            })
            response = r.json()
            status_code = r.status_code
            if status_code == HTTP_200_OK:
                res = redirect('home')
                res.set_cookie('token', response.get('token'))
                return res
            elif status_code == HTTP_400_BAD_REQUEST:
                messages.info(request, 'Please fill in correct unique Username, Email and valid Password!')
        else:
            messages.info(request, 'Please fill match Password!')

    return render(request, 'authen/register.html', None)    

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
            res = redirect('home')
            res.set_cookie('token', response.get('token'))
            return res
        else:
            if username == '' or password == '':
                messages.info(request, 'Please fill in Username and Password!')
            else:
                messages.info(request, 'Please fill in correct Username and Password!')
            return render(request, 'authen/login.html')
    else:
        return render(request, 'authen/login.html')

def logout(request):
    res = redirect('login')
    res.delete_cookie('token')
    return res

def home(request):
    token = request.COOKIES.get('token')
    result = requests.get('http://localhost:8000/api/user/info', headers={
        'Authorization': 'Bearer %s' % token,
    })
    status_code = result.status_code
    response = result.json()
    if status_code != HTTP_200_OK:
        res = redirect('login')
        res.delete_cookie('token')
        return res
    res = render(request, 'home/index.html')
    res.set_cookie('username', response['username'])
    res.set_cookie('email', response['email'])
    return res
