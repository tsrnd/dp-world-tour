from django.urls import path, include

urlpatterns = [
    path('user/', include('clients.users.urls')),
    path('stadium/', include('clients.stadium.urls')),
    path('match/', include('clients.matches.urls')),
    path('team/', include('clients.teams.urls')),
    path('booking/', include('clients.booking.urls'))
]
