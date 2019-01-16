from django.urls import path, re_path
from myapp.user.handlers import AuthHandler, AdminView, UserRetrieveUpdateAPIView, TokenView
from myapp.serializer.auth_serializer import MyAppTokenObtainPairView

urlpatterns = [
    path('register', AuthHandler.as_view(), name='register'),
    re_path(r'^update/?$', UserRetrieveUpdateAPIView.as_view(), name='update'),
    path('admin-view', AdminView.as_view(), name='admin'),
    re_path(r'^token/?$', TokenView.as_view(), name='token'),
    re_path(r'^login/?$', MyAppTokenObtainPairView.as_view(), name='token')
]
