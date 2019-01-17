from django.urls import path
from snippets.serializers import UserSerializer

from clients.users import views

urlpatterns = [
    path('register', views.register),
    path('create', views.create_user),
    path('login', views.login),
]
