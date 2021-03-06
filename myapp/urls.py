from django.urls import path, include

urlpatterns = [
    path('stadium/', include('myapp.stadium.urls')),
    path('user/', include('myapp.user.urls')),
    path('match/', include('myapp.match.urls')),
    path('team/', include('myapp.team.urls')),
    path('booking/', include('myapp.booking.urls')),
]
