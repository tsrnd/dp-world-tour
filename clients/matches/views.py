from django.shortcuts import render
import requests
import json
from datetime import datetime
from clients.matches.forms import FindMatchForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

def index(request):
    toDay = datetime.now().strftime("%Y-%m-%d")
    response = render(request, 'match/match.html', {'today': toDay})
    return response


def find_match(request):
    token = request.COOKIES.get('token')
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
                print(response)
                if r.status_code == 201:
                    messages.add_message(request, messages.SUCCESS, _('Đã đăng kí tìm kiếm trận đấu thành công.'))
                elif r.status_code == 400:
                    messages.add_message(request, messages.ERROR, _('Mời bạn chọn lịch thi đấu khác'))
                else:
                    messages.add_message(request, messages.ERROR, _('Tìm kiếm trận đấu thất bại.'))
                return render(request, 'match/match.html', None)
    messages.add_message(request, messages.ERROR, _('Tìm kiếm trận đấu thất bại.'))
    return render(request, 'match/match.html', {'form': form})
