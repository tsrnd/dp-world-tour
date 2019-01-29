from django.urls import path

from clients.booking import views

urlpatterns = [
    path('list/', views.my_list_booking)
]
