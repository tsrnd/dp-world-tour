import inject
from myapp.team.serializers import TeamCreateSerializer

from myapp.models.teams import Team
from shared.base_handler import BaseHandler

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

class TeamCreate(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = TeamCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Create team successfully"
        }
        return Response(
            context,
            status=status.HTTP_201_CREATED,
        )
