from django.urls import path
from myapp.stadium.handlers import StadiumHandler

urlpatterns = [
    path('list', StadiumHandler.as_view(), name='stadium_list'),
]
