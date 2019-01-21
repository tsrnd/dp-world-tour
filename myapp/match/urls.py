from django.urls import path
from myapp.match.handlers import FindMatchAPIView
urlpatterns = [
    path('', FindMatchAPIView.as_view(), name='find-match'),
]
