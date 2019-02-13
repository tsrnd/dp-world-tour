from django.urls import path
from myapp.stadium.handlers import StadiumHandler
from myapp.stadium.stadium_detail_views import StadiumDetailView
from myapp.stadium.booking_views import BookingView
from django.conf.urls import url


urlpatterns = [
    url(r'^list$', StadiumHandler.as_view(), name='stadium_list'),
    url(r'^(?P<pk>\d+)/book/$', BookingView.as_view(), name='bookingviews'),
    path('<int:stadiumID>/detail/', StadiumDetailView.as_view()),
]
