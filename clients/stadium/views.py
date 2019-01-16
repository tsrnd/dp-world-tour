from django.shortcuts import render
import requests, json

def get_list(request):
    return render(request, 'stadium/stadium_list.html', None)

# def create_user(request):
#     r = requests.post('http://localhost:8000/api/user/register', data={
#         'email': 'test',
#         'user_name': 'test',
#         'password': 'test',
#     })
#     response = r.json()
#     print(response["message"])
#     return render(request, 'authen/login.html', None)
