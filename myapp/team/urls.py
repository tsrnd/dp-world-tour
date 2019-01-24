from django.urls import path
from django.conf.urls import url

from myapp.team.handlers import (
    TeamCreate, TeamList, InvitationList, InvitationUpdate
)

urlpatterns = [
    path('create', TeamCreate.as_view(), name='create-team'),
    path('', TeamList.as_view(), name='list-team'),
    path('invitation', InvitationList.as_view(), name='list-invitation'),
    url(r'^invitation/(?P<pk>\d+)$', InvitationUpdate.as_view(), name='update-invitation'),
]
