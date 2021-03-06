from django.shortcuts import render, redirect
import requests, json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib import messages
from django.shortcuts import redirect
from myapp.models.user_teams import UserTeam
RESULT_LIMIT = 50


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
    re = requests.get('http://localhost:8000/api/team/invitation', headers={
        'Authorization': 'Bearer %s' % token,
    })
    invitations = re.json()
    return render(request, 'team/team_list.html', {'teams':teams, 'invitations': invitations})

def get_users_invite(request, id):
    token = request.COOKIES.get('token')
    if token is None:
        messages.info(request, 'You must log in this website!')
        return redirect('login')
    else:
        page = request.GET.get('page', 1)
        result_limit = request.GET.get('result_limit', RESULT_LIMIT)
        payload = {'page': page, 'result_limit': result_limit}

        headers = {
            'Authorization': 'Bearer %s' % token
        }
        result = requests.get('http://127.0.0.1:8000/api/team/'+ str(id) +'/list_users_invite', headers=headers, params=payload)
        status_code = result.status_code
        users = result.json()
        for index, user in enumerate(users['result']):
            user['stt'] = (int(page)-1) * RESULT_LIMIT + index + 1
        if (status_code == HTTP_200_OK and users['id_team'] == id):
            return render(request, 'team/invite_member.html',{'users': users}) 
        else:
            messages.info(request, 'Please create a team with roll Caption to have permission invite member!')
            return redirect('team-register')
