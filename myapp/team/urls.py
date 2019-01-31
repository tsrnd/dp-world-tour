from django.urls import path
from django.conf.urls import url

from myapp.team.handlers import (
    TeamCreate, TeamList, InvitationList, InvitationUpdate, ListUserInvite, InviteMember,
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team'),
    path('', TeamList.as_view(), name='list-team'),
    path('invitation', InvitationList.as_view(), name='list-invitation'),
    url(r'^invitation/(?P<pk>\d+)$', InvitationUpdate.as_view(), name='update-invitation'),
    path('list_users_invite', ListUserInvite.as_view(), name='list_users_invite'),
    path('invite', InviteMember.as_view(), name='invite_member')
]
