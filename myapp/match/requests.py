from rest_framework import serializers
from myapp.models.user_teams import UserTeam

class FindMatchSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=10)


class UserTeamSerializer(serializers.Serializer):
    class Meta:
        model = UserTeam