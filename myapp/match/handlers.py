import inject
import json
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from shared.base_handler import *
from myapp.match.requests import (
    FindMatchSerializer,
    MatchAcceptSerializer,
    FindMatchListSerializer,
    MatchDetailSerializer,
)
from myapp.models.matches import (
    Match,
)
from myapp.models.find_matches import FindMatch
from myapp.models.user_teams import UserTeam
from rest_framework.permissions import IsAuthenticated
from myapp.permission.match_permission import IsLeadTeam
from myapp.permission.user_permission import IsNormalUser
logger = logging.getLogger(__name__)

class FindMatchAPIView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = FindMatchSerializer
    permission_classes = (IsAuthenticated,IsLeadTeam,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Create find match successfully"
        }
        return Response(
            context,
            status=status.HTTP_201_CREATED,
        )

class MatchUpdate(UpdateModelMixin, GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = MatchAcceptSerializer
    permission_classes = [IsAuthenticated, IsNormalUser, IsLeadTeam, ]
    lookup_field = 'pk'
    queryset = Match.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=kwargs, partial=True)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Update match successfully"
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

class MatchList(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = FindMatchListSerializer
    permission_classes = (IsAuthenticated, IsNormalUser, IsLeadTeam, )

    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(user=self.request.user)
        team_ids = []
        for team in teams.iterator():
            team_ids.append(team.team_id)
        matches = FindMatch.objects.filter(team_id__in=team_ids).order_by("-status", "created_at")
        serializer = self.get_serializer(matches, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class FindMatchDetail(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = MatchDetailSerializer
    permission_classes = (IsAuthenticated, IsNormalUser, IsLeadTeam, )

    def get(self, request, *args, **kwargs):
        find_match = get_object_or_404(FindMatch, pk=kwargs['id'])
        match = Match.objects.filter(Q(find_match_a_id=find_match.id)|Q(find_match_b_id=find_match.id))
        serializer = self.get_serializer(match[0])
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
