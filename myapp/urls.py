from django.urls import path, include, re_path
urlpatterns = [
    path('user/', include('myapp.user.urls')),
]
