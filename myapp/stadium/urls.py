from django.conf.urls import url

from myapp.stadium.booking_views import BookingView

urlpatterns = [
    url(r'^(?P<pk>\d+)/book/$', BookingView.as_view(), name='bookingviews'),
]
