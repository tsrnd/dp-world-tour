from django.urls import path
from django.conf.urls import url
from myapp.match.handlers import (
    FindMatchAPIView,
    MatchUpdate,
    MatchList,
    FindMatchDetail,
)
urlpatterns = [
    path('', FindMatchAPIView.as_view(), name='find-match'),
    path('history', MatchList.as_view(), name='history-match'),
    url(r'^(?P<pk>\d+)$', MatchUpdate.as_view(), name='match-update'),
    path('<int:id>/detail', FindMatchDetail.as_view(), name='find-match-detail'),
]
