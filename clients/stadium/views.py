from django.shortcuts import render
from myapp.models.stadiums import Stadium
from django.contrib import messages
from shared import utils
from datetime import datetime
import requests
import requests, json
from datetime import datetime, date, time, timedelta
from django.contrib import messages



class Stadium2:
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email

    @staticmethod
    def fakeStadium():
        return Stadium2("Catch position cold. Begin article can military establish.", "0349566507", "lam.le@asiantech.vn")


def myBookingView(request, stadiumID):
    # Handle with stadium ID
    token = request.COOKIES.get('token')
    r = requests.get('http://localhost:8000/api/stadium/{}/detail/'.format(stadiumID))
    stadium = r.json()
    if token == None:
        # Show warning message to login
        messages.add_message(
            request, messages.ERROR, 'Please login again')
        # return render(request, 'stadium/booking.html', {
        #     'stadium': stadium, 'stadiumID': stadiumID
        # })
    else:
        if request.method == 'GET':
            return render(request, 'stadium/booking.html', {
                'stadium': stadium, 'stadiumID': stadiumID
            })
        elif request.method == 'POST':
            timeFrom, timeTo = request.POST.get(
                'time_from'), request.POST.get('time_to')
            if not timeFrom:  # Check time_from is empty
                timeFrom = utils.convertTimestampToString(
                    utils.currentTimestamp())
            if not timeTo:  # Check time_to is empty
                timeTo = utils.convertTimestampToString(
                    utils.convertStringToTimestamp(timeFrom) + 3600)
            # headers for request
            headers = {'Authorization': 'Bearer %s' % token}
            # Data for request
            data = {"time_from": timeFrom, "time_to": timeTo}
            r = requests.post(
                'http://localhost:8000/api/stadium/{}/book/'.format(stadiumID), data=data, headers=headers)
            if r.status_code == 201:
                messages.add_message(
                    request, messages.SUCCESS, 'Register stadium successfully')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Register stadium failure')
            return render(request, 'stadium/booking.html', {
                'stadium': stadium,
                'stadiumID': stadiumID,
                'time_from': timeFrom,
                'time_to': timeTo
            })
        else:
            messages.add_message(request, messages.SUCCESS,
                                 'Please use GET or POST method')
            return render(request, 'stadium/booking.html', {
                'stadium': stadium, 'stadiumID': stadiumID
            })

def convert(time):
    return int(datetime.strptime(time, '%Y-%m-%d %H:%M+00').strftime('%s'))


def get_list(request):
    time_from = request.POST.get("time_from")
    time_to = request.POST.get("time_to")
    min_price = request.POST.get("min_price")
    max_price = request.POST.get('max_price')
    result_limit = request.POST.get("result_limit", 20)
    page = request.GET.get('page', 1)
    old_input = {}
    old_input['time_from'] = time_from
    old_input['time_to'] = time_to
    old_input['min_price'] = min_price
    old_input['max_price'] = max_price
    old_input['result_limit'] = result_limit
    if time_from == '' or time_from is None:
        time_from = int(datetime.now().strftime('%s'))
    else:
        time_from = convert(time_from)
    if time_to == '' or time_to is None:
        time_to = time_from + 3600
    else:
        time_to = convert(time_to)
    if time_from < int(datetime.now().strftime('%s')):
        messages.info(request, 'Vui lòng nhập thời gian bắt đầu lớn hơn thời gian hiện tại')
    elif time_from >= time_to:
        messages.info(request, 'Vui lòng nhập thời gian kết thúc lớn hơn thời gian bắt đầu')
    response = requests.get('http://localhost:8000/api/stadium/list', params={
        'time_from': time_from,
        'time_to': time_to,
        'min_price': min_price,
        'max_price': max_price,
        'page': page,
        'result_limit': result_limit,
    })
    stadiums = response.json()
    return render(request, 'stadium/stadium_list.html', {'stadiums':stadiums, 'old_input': old_input})
