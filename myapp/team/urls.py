from django.conf.urls import url

from myapp.team.handlers import (
    TeamCreate,
)

urlpatterns = [
    url(r'^create/$', TeamCreate.as_view(), name='create'),
]
