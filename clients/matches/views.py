from django.shortcuts import render
import requests
import json
from datetime import datetime
from clients.matches.forms import FindMatchForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def index(request):
    today = datetime.now().strftime("%Y-%m-%d")
    response = render(request, 'match/match.html', {'today': today})
    return response


def find_match(request):
    token = request.COOKIES.get('token')
    today = datetime.now().strftime("%Y-%m-%d")
    if token != None:
        if request.method == 'POST':
            form = FindMatchForm(request.POST)
            if form.is_valid():
                date_match = form.cleaned_data['date_match'].strftime("%s")
                headers = {'Authorization': 'Bearer %s' % token}
                r = requests.post('http://localhost:8000/api/match/', data={
                    'date_match': date_match,
                }, headers=headers)
                response = r.json()
                if r.status_code == 201:
                    messages.add_message(request, messages.SUCCESS, _(
                        'Đã đăng kí tìm kiếm trận đấu thành công.'))
                elif r.status_code == 400:
                    messages.add_message(request, messages.ERROR, _(
                        'Mời bạn chọn lịch thi đấu khác'))
                else:
                    messages.add_message(request, messages.ERROR, _(
                        'Tìm kiếm trận đấu thất bại.'))
                return render(request, 'match/match.html', {'today': today})
    messages.add_message(request, messages.ERROR,
                         _('Tìm kiếm trận đấu thất bại.'))
    return render(request, 'match/match.html', {'form': form, 'today': today})

def find_match_history(request):
    token = request.COOKIES.get('token')
    if token != None:
        headers = {'Authorization': 'Bearer %s' % token}
        r = requests.get('http://localhost:8000/api/match/history', headers=headers)
        response = r.json()
        print("response: ", response)
        return render(request, 'match/find_history.html', {
            'histories': response,
        })
                
    return render(request, 'authen/login.html')

def find_match_detail(request, id):
    token = request.COOKIES.get('token')
    if token != None:
        headers = {'Authorization': 'Bearer %s' % token}
        r = requests.get('http://localhost:8000/api/match/' + str(id) + '/detail', headers=headers)
        response = r.json()
        print("response: ", response)
        return render(request, 'match/match_detail.html', {'response': response})
                
    return render(request, 'authen/login.html')
