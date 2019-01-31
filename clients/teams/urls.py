from django.urls import path

from clients.teams import views

urlpatterns = [
    path('register', views.register, name='team-register'),
    path('list', views.list, name='team-list'),
    path('<int:id>/invite_member', views.get_users_invite, name='invite_member'),
]
