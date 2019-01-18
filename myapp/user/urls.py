from django.urls import path
from myapp.user.handlers import AuthHandler,LoginUser

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
]
