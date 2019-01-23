from django.urls import path, include

urlpatterns = [
    path('user/', include('clients.users.urls')),
    path('team/', include('clients.teams.urls'))
]
