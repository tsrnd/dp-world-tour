from django.shortcuts import render
import requests, json

def register(request):
    return render(request, 'team/create_team.html', None)

def list(request):
    return render(request, 'team/team_list.html', None)
