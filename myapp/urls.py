from django.urls import path, include

urlpatterns = [
    path('stadium/', include('myapp.stadium.urls')),
    path('user/', include('myapp.user.urls'))
]
