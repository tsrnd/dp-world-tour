from django.shortcuts import render
from myapp.models.stadiums import Stadium
import requests


class Stadium2:
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email


def myBookingView(request, stadiumID):
    timeFrom = ""
    timeTo = ""
    if request.method == "POST":
        # Get time from and time to
        timeFrom = request.POST.get('time_from')
        timeTo = request.POST.get('time_to')
        print("timeFrom=", timeFrom)
        print("timeTo=", timeTo)
        # Call response
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer db59da58dd51b30253ee4580e65b4cd8140a68c4'}
        data = {
            "time_from": timeFrom,
            "time_to": timeTo,
        }
        response = requests.post(
            'http://localhost:8000/api/stadium/{}/book/'.format(stadiumID), data=data, headers=headers)
        print(response.status_code)
        if timeFrom == '':
            timeFrom = "Invalid"
            print("handle none")
        else:
            print("handle time to")
        if timeTo == '':
            timeTo = "Invalid"
            print("Handle none")
        else:
            # Call api post
            print("time")
    elif request.method == "GET":

        print('This is get method')
    else:
        return handleError(request, 'Only show screen with POST and GET')
    # Test stadium
    stadium = Stadium2(
        "Catch position cold. Begin article can military establish.", "0349566507", "lam.le@asiantech.vn")
    return render(request, 'stadium/booking.html', {
        'stadium': stadium,
        'stadiumID': stadiumID,
        'timeFrom': timeFrom,
        'timeTo': timeTo,
    })


def handleError(request, errorDescription):
    return render(request, 'stadium/booking_error.html', {
        'error': errorDescription
    })


def handlePostOnMyBookingView(request, stadiumID):
    pass


def handleGetOnMyBookingView(request, stadiumID):
    pass
