from django.urls import re_path

from clients.booking import views

urlpatterns = [
    re_path('list/(?:page-(?P<page>\d+)/)?$', views.my_list_booking, name='list')
    
]
