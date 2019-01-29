from django.urls import path

from myapp.team.handlers import (
    TeamCreate, InviteMember,
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team'),
    path('list_member', InviteMember.as_view(), name='invite-member'),
]
