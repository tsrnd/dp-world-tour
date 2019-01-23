from django.urls import path

from myapp.team.handlers import (
    TeamCreate, TeamList
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team'),
    path('', TeamList.as_view(), name='list-team'),
]
