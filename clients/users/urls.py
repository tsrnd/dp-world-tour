from django.urls import path

from clients.users import views

urlpatterns = [
    path('register', views.register),
    path('create', views.create_user),
]
