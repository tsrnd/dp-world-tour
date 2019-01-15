from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from myapp.serializer.auth_serializer import MyAppTokenObtainPairView
urlpatterns = [
    path('user/', include('myapp.user.urls')),
    re_path(r'^token/$', MyAppTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
