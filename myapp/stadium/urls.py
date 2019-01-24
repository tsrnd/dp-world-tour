from django.urls import path
from myapp.stadium import views
from myapp.stadium.stadium_detail_views import StadiumDetailView

urlpatterns = [
    path('<int:stadiumID>/detail/', StadiumDetailView.as_view()),
]
