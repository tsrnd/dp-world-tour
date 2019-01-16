from django.shortcuts import render
import requests, json

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