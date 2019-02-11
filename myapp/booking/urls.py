from django.urls import path
from django.conf.urls import url
from myapp.booking.booking_detail import BookingDetail

urlpatterns = [
    url(r'^(?P<id_booking>\d+)/detail/$',
        BookingDetail.as_view(), name='bookingviews'),
]
