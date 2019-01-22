from myapp.team.serializers import TeamCreateSerializer

from myapp.models.teams import Team

from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

class TeamCreate(CreateAPIView):
    parser_classes = (MultiPartParser, )
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    permission_classes = [IsAuthenticated]
