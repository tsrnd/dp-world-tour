from django.urls import path

from myapp.team.handlers import (
    TeamCreate, TeamList, InvitationList
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team'),
    path('', TeamList.as_view(), name='list-team'),
    path('invitation', InvitationList.as_view(), name='list-invitation'),
]
