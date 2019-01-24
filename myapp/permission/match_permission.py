from rest_framework.permissions import BasePermission
from myapp.models.user_teams import UserTeam
from rest_framework.exceptions import PermissionDenied
from rest_framework import exceptions

class IsLeadTeam(BasePermission):
    message = {'message': 'User is not role CAPTION in team'}

    def has_permission(self, request, view):
        try:
            userTeam = UserTeam.objects.get(user__pk =request.user.id, roll ="CAPTION")
            if not request.POST._mutable:
                request.POST._mutable = True
            request.data['team_id'] = userTeam.team.id
            return True
        except UserTeam.DoesNotExist:
            return False
