from django.urls import path
from myapp.user.handlers import AuthHandler, AuthenticateUser

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
    path('token', AuthenticateUser.as_view(), name='token'),
]
