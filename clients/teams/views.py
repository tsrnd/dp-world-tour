from django.shortcuts import render, redirect
import requests

def register(request):
    return render(request, 'team/create_team.html', None)

def list(request):
    token = request.COOKIES.get('token')
    if token is None:
        return redirect('login')
    r = requests.get('http://localhost:8000/api/team', headers={
        'Authorization': 'Bearer %s' % token,
    })
    teams = r.json()
    return render(request, 'team/team_list.html', {'teams':teams})
