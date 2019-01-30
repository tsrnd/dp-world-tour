from django.shortcuts import render, redirect
from rest_framework import status
import requests

# Define result limit


def result_limit():
    return 2


def my_list_booking(request):
    token = request.COOKIES.get('token')
    if token is None:
        return redirect('login')
    headers = {'Authorization': 'Bearer %s' % token}
    if request.method == 'POST':
        page = int(request.POST.get('page'))
    else:
        page = 1
    r = requests.get(
        'http://localhost:8000/api/booking?result_limit={}&page={}'.format(result_limit(), page), headers=headers)
    if r.status_code == status.HTTP_200_OK:
        bookings = r.json()['bookings']
        for index, booking in enumerate(bookings):
            booking['stt'] = (page-1) * result_limit() + index + 1
        return render(request, 'booking/list.html', {
            "bookings": bookings,
            'page': page,
            'next_page_flg': r.json()['next_page_flg'],
            'result_limit': result_limit()
        })
    return render(request, 'booking/list.html', {
        'page': page
    })
