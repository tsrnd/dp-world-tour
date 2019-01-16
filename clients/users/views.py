from django.shortcuts import render
import requests, json

def register(request):
    return render(request, 'authen/register.html', None)

def create_user(request):
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
        return render(request, 'authen/login.html', response)
    else :
        return render(request, 'authen/register.html',None)
