from django.urls import path

from .booking_views import BookingView

urlpatterns = [
    # Please check name in bookings view
    path('<int:pk>/booking/', BookingView.as_view(), name='booking_views')
]
