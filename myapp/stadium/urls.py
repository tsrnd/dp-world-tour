from django.urls import path
from myapp.stadium.handlers import StadiumHandler
from django.conf.urls import url

from myapp.stadium.booking_views import BookingView

urlpatterns = [
    url(r'^list$', StadiumHandler.as_view(), name='stadium_list'),
    url(r'^(?P<pk>\d+)/book/$', BookingView.as_view(), name='bookingviews'),
]
