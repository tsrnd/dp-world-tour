from django.urls import path
from myapp.user.handlers import AuthHandler, UserLoginAPIView,UserInfoAPIView,UserRegisterAPIView

urlpatterns = [
    path('register', UserRegisterAPIView.as_view(), name='register'),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('info', UserInfoAPIView.as_view(), name='info'),
]
