from django.urls import path
from myapp.booking.list_booking_views import ListBookingView
from myapp.booking.booking_cancel_views import BookingCancel
from django.conf.urls import url

urlpatterns = [
    path('', ListBookingView.as_view(), name='list_booking'),
    url(r'^(?P<pk>\d+)/cancel$', BookingCancel.as_view(), name='booking_cancel'),
]
