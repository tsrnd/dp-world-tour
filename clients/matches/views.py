from django.shortcuts import render
import requests
import json
from clients.matches.forms import FindMatchForm
from django.contrib import messages

def index(request):
    response = render(request, 'match/match.html', None)
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
                if r.status_code == 200:
                    messages.add_message(request, messages.SUCCESS, 'Đã đăng kí tìm kiếm trận đấu thành công.')
                elif r.status_code == 400:
                    messages.add_message(request, messages.ERROR, 'Mời bạn chọn lịch thi đấu khác')
                else:
                    messages.add_message(request, messages.ERROR, 'Tìm kiếm trận đấu thất bại.')
                return render(request, 'match/match.html', None)
    messages.add_message(request, messages.ERROR, 'Tìm kiếm trận đấu thất bại.')
    return render(request, 'match/match.html', {'form': form})
