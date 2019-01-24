from django.urls import path, include
from clients.matches import views

urlpatterns = [
    path('', views.index, name='find-match'),
    path('find', views.find_match, name='find-match-request'),
]
