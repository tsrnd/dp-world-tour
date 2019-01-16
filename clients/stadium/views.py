from django.shortcuts import render
import requests, json
from datetime import datetime
from datetime import datetime, date, time, timedelta

def convert(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S+00').timestamp()


def get_list(request):
    time_from = request.POST.get("time_from")
    time_to = request.POST.get("time_to")
    price = request.POST.get("price")
    print(time_from)
    if time_from == '' or time_from is None:
        time_from = datetime.now().timestamp()
    else:
        time_from = convert(time_from)
    if time_to == '' or time_to is None:
        time_to = time_from + 3600
    else:
        time_to = convert(time_to)
    response = requests.get('http://localhost:8000/api/stadium/list', data={
        'time_from': time_from,
        'time_to': time_to,
        'price': price,
    })
    stadiums = response.json()
    return render(request, 'stadium/stadium_list.html', {'stadiums':stadiums})
