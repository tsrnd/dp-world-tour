from django.urls import path

from clients.teams import views

urlpatterns = [
    path('register', views.register),
    path('list', views.list),
]
