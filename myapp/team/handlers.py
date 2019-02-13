import inject
from myapp.team.serializers import (
    TeamCreateSerializer, UserTeamSerializer,
    InvitationListSerializer, InvitationUpdateSerializer, InviteSerializer, InviteMemberSerializer, 
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
from myapp.permission.match_permission import(
    IsLeadTeam,
)
from myapp.permission.user_permission import (
    IsNormalUser,
)
from myapp.permission.match_permission import (
    IsLeadTeam,
)
from rest_framework.authtoken.models import Token
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from myapp.models.user_teams import UserTeam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

RESULT_LIMIT = 50
PAGE_DEFAULT = 1

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

class ListUserInvite(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated, IsLeadTeam]

    def get(self, request, id):
        id_team = request.data['team_id']
        if id == id_team:
            users_list = User.objects.filter(~Q(userteam__team_id=id_team), is_superuser = False).order_by('date_joined')

            result_limit = request.GET.get('result_limit', RESULT_LIMIT)
            page = request.GET.get('page', PAGE_DEFAULT)
            paginator = Paginator(users_list, result_limit)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(PAGE_DEFAULT)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            serializer = InviteSerializer(users, many=True)

            content = {
                'id_team': id_team,
                'result_count': users_list.count(),
                'page': int(page),
                'next_page_flg': users.has_next(),
                'result': serializer.data,
            }
            return Response(content)
        else: 
            context = {
                "message": "Forbiden"
            }
            return Response(
                context,
                status=status.HTTP_403_FORBIDDEN
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

class InviteMember(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = InviteMemberSerializer
    permission_classes = [IsAuthenticated, IsLeadTeam]

    def post(self, request, id):
        from django.db import transaction
        user_id = request.POST.get('user_id')
        id_team = request.data['team_id']
        if id == id_team:
            user = User.objects.get(pk=user_id)
            team = Team.objects.get(pk=id_team)
            with transaction.atomic():
                invite_member = UserTeam.objects.create(
                    team = team,
                    user = user,
                    roll = 'MEMBER',
                    status = 'PENDING',
                )
            serializer = InviteMemberSerializer(team)
            context = {
                'message': 'Invite member successfull!'
            }
            return Response(
                context,
                status=status.HTTP_201_CREATED,
            )
        else: 
            context = {
                "message": "Forbiden"
            }
            return Response(
                context,
                status=status.HTTP_403_FORBIDDEN
            )
