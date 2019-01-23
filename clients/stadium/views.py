from django.shortcuts import render
import requests, json
from datetime import datetime
from datetime import datetime, date, time, timedelta
from django.contrib import messages

def convert(time):
    return int(datetime.strptime(time, '%Y-%m-%d %H:%M+00').strftime('%s'))


def get_list(request):
    time_from = request.POST.get("time_from")
    time_to = request.POST.get("time_to")
    price = request.POST.get("price", '')
    result_limit = request.POST.get("result_limit", 20)
    page = request.GET.get('page', 1)
    if time_from == '' or time_from is None:
        time_from = int(datetime.now().strftime('%s'))
    else:
        time_from = convert(time_from)
    if time_to == '' or time_to is None:
        time_to = time_from + 3600
    else:
        time_to = convert(time_to)
    if time_from > time_to:
        messages.info(request, 'Please fill time to great than time from')
    response = requests.get('http://localhost:8000/api/stadium/list', params={
        'time_from': time_from,
        'time_to': time_to,
        'price': price,
        'page': page,
        'result_limit': result_limit,
    })
    stadiums = response.json()
    return render(request, 'stadium/stadium_list.html', {'stadiums':stadiums})

