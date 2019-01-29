from django.urls import path
from clients.teams import views

urlpatterns = [
    path('register', views.register),
    path('list', views.list),
    path('invite_member', views.get_users_invite, name='invite_member'),
]
