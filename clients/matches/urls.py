from django.urls import path, include
from clients.matches import views

urlpatterns = [
    path('', views.index),
    path('find', views.find_match)
]
