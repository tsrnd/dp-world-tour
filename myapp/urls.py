from django.urls import path, include

urlpatterns = [
    path('user/', include('myapp.user.urls')),
    path('stadium/', include('myapp.stadium.urls'))
]
