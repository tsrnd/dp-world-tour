from django.urls import path, include
from clients.matches import views

urlpatterns = [
    path('', views.index, name='find-match'),
    path('find', views.find_match, name='find-match-request'),
    path('history', views.find_match_history, name='find-match-history'),
    path('<int:id>/detail/', views.find_match_detail, name='find-match-detail'),
]
