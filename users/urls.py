from django.urls import path, re_path
from .views import CreateUserAPIView, UserRetrieveUpdateAPIView
from . import views

urlpatterns = [
    re_path(r'^create/?$', CreateUserAPIView.as_view(), name='create'),
    re_path(r'^token/?$', views.authenticate_user, name='token'),
    re_path(r'^update/?$', UserRetrieveUpdateAPIView.as_view(), name='update'),
]