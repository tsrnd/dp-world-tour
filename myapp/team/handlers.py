import inject
from myapp.team.serializers import (
    TeamCreateSerializer, UserTeamSerializer,
    InvitationListSerializer, InvitationUpdateSerializer,
)

from myapp.models.teams import Team
from myapp.models.user_teams import UserTeam
from django.db.models import Q
from shared.base_handler import BaseHandler

from rest_framework.parsers import (
    MultiPartParser, FormParser
)

from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from myapp.permission.user_permission import (
    IsNormalUser,
)

class TeamCreate(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = TeamCreateSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, ]

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

class TeamList(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = UserTeamSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, ]

    def get(self, request, *args, **kwargs):
        user_teams = UserTeam.objects.filter(user=self.request.user, status='ACCEPTED').order_by('roll')
        serializer = self.get_serializer(user_teams, many=True)
        context = []
        if len(serializer.data) != 0:
            for team in serializer.data:
                team_tmp = team['team']
                team_tmp['is_caption'] = team['is_caption']
                context.append(team_tmp)
        return Response(
            context,
            status=status.HTTP_200_OK,
        )

class InvitationList(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = InvitationListSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, ]

    def get(self, request, *args, **kwargs):
        user_teams = UserTeam.objects.filter(user=self.request.user).filter(Q(status='PENDING')|Q(status='REJECTED')).order_by('status', '-created_at')
        serializer = self.get_serializer(user_teams, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class InvitationUpdate(UpdateModelMixin, GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = InvitationUpdateSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, ]
    lookup_field = 'pk'
    queryset = UserTeam.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=kwargs, partial=True)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Update invitation successfully"
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        kwargs['status'] = 'ACCEPTED'
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        kwargs['status'] = 'REJECTED'
        return self.update(request, *args, **kwargs)
