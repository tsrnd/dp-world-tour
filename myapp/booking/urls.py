from django.urls import path
from django.conf.urls import url

from myapp.booking.handlers import (
    BookingCancel
)

urlpatterns = [
    url(r'^(?P<pk>\d+)/cancel$', BookingCancel.as_view(), name='booking_cancel'),
]
