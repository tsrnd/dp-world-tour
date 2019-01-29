from django.shortcuts import render


def my_list_booking(request):
    return render(request, 'booking/list.html')
