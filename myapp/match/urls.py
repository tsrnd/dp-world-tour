from django.urls import path
from django.conf.urls import url
from myapp.match.handlers import (
    FindMatchAPIView,
    MatchUpdate,
)
urlpatterns = [
    path('', FindMatchAPIView.as_view(), name='find-match'),
    url(r'^(?P<pk>\d+)$', MatchUpdate.as_view(), name='match-update'),
]
