from django.urls import path, include

urlpatterns = [
    path('user/', include('myapp.user.urls')),
    path('matches/', include('myapp.match.urls'))
]
