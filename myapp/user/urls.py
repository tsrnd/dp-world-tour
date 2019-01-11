from django.urls import path
from myapp.user.handlers import AuthHandler

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
]
