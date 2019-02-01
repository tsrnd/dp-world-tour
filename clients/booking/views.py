from django.shortcuts import render, redirect
from rest_framework import status
from shared import utils
import requests

# Define result limit
RESULT_LIMIT = 20
DATE_FORMAT = '%d/%m/%Y %H:%M'


def my_list_booking(request, page):
    # Get token
    token = request.COOKIES.get('token')
    if token is None:
        return redirect('login')

    # Call api
    headers = {'Authorization': 'Bearer %s' % token}
    if request.method == 'POST':
        page = int(request.POST.get('page'))
    else:
        page = int(request.GET.get('page'))
    r = requests.get(
        'http://localhost:8000/api/booking?result_limit={}&page={}'.format(RESULT_LIMIT, page), headers=headers)

    # Handle response
    if r.status_code == status.HTTP_200_OK:
        bookings = r.json()['bookings']
        for index, booking in enumerate(bookings):
            booking['stt'] = (page-1) * RESULT_LIMIT + index + 1
            booking['time_from'] = utils.convertTimestampToString(
                int(booking['time_from']), dateFormat=DATE_FORMAT)
            booking['time_to'] = utils.convertTimestampToString(
                int(booking['time_to']), dateFormat=DATE_FORMAT)
        return render(request, 'booking/list.html', {
            "bookings": bookings,
            'page': page,
            'next_page_flg': r.json()['next_page_flg'],
            'result_limit': RESULT_LIMIT
        })
    return render(request, 'booking/list.html', {
        'page': page
    })
