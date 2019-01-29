from django.urls import path
from myapp.booking.list_booking_views import ListBookingView

urlpatterns = [
    path('', ListBookingView.as_view())
]
