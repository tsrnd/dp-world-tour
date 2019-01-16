from django.urls import path

from clients.stadium import views

urlpatterns = [
    path('list', views.get_list, name="list"),
]
