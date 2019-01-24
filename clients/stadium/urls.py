from django.urls import path

from clients.stadium import views

urlpatterns = [
    path('<int:stadiumID>/booking/', views.myBookingView, name='booking'),
]
