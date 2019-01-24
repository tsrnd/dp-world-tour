from django.urls import path, include

urlpatterns = [
    path('user/', include('myapp.user.urls')),
    path('match/', include('myapp.match.urls')),
    path('team/', include('myapp.team.urls')),
]
