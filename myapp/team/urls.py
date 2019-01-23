from django.urls import path

from myapp.team.handlers import (
    TeamCreate,
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team')
]
