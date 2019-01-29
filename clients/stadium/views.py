from django.shortcuts import render
from myapp.models.stadiums import Stadium
from django.contrib import messages
from shared import utils
from datetime import datetime
import requests


def myBookingView(request, stadiumID):
    # Handle with stadium ID
    token = request.COOKIES.get('token')
    r = requests.get(
        'http://localhost:8000/api/stadium/{}/detail/'.format(stadiumID))
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
            messages.add_message(request, messages.ERROR,
                                 'Please use GET or POST method')
            return render(request, 'stadium/booking.html', {
                'stadium': stadium, 'stadiumID': stadiumID
            })
