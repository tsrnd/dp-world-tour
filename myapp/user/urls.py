from django.urls import path, re_path
from myapp.user.handlers import AuthHandler
from myapp.serializer.auth_serializer import AuthenticateSerializerView

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
    re_path(r'^login/?$', AuthenticateSerializerView.as_view(), name='token')
]
