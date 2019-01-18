from django.urls import path

from clients.users import views

urlpatterns = [
    path('register', views.register),
    path('create', views.create_user),
    path('login', views.login, name='login'),
    path('home', views.home, name='home')
]
