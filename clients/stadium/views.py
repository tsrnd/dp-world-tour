from django.shortcuts import render
import requests, json

def get_list(request):
    response = requests.get('http://localhost:8000/api/stadium/list')
    stadiums = response.json()
    return render(request, 'stadium/stadium_list.html', {'stadiums':stadiums})

