from django.shortcuts import render, redirect
import requests


def my_list_booking(request):
    token = request.COOKIES.get('token')
    if token is None:
        return redirect('login')
    headers = {'Authorization': 'Bearer %s' % token}
    result_limit = 20
    page = 1
    r = requests.get(
        'http://localhost:8000/api/booking?result_limit={}&page={}'.format(result_limit, page), headers=headers)
    bookings = r.json()['bookings']
    for index, booking in enumerate(bookings):
        booking['stt'] = index + 1
    return render(request, 'booking/list.html', {
        "bookings": bookings
    })
