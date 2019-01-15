from django.urls import path, re_path
from myapp.user.handlers import AuthHandler, AdminView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
    re_path(r'^update/?$', UserRetrieveUpdateAPIView.as_view(), name='update'),
    path('admin-view', AdminView.as_view(), name='admin'),
]
