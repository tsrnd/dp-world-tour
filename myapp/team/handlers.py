import inject
from myapp.team.serializers import TeamCreateSerializer, InviteSerializer

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

class InviteMember(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id_user_login = self.request.user.id
        id_team= get_object_or_404(Team,userteam__user_id=id_user_login, userteam__roll='CAPTION')
        users_list = User.objects.exclude(userteam__team_id=id_team).order_by('date_joined')

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
            'links': {
                'has_other_pages': users.has_other_pages(),
                'has_previous': users.has_previous(),
                'has_next': users.has_next(),
                'num_pages': paginator.num_pages,
            },
            'result_count': users_list.count(),
            'page': page,
            'next_page_flg': users.has_next(),
            'result': serializer.data,
        }
        return Response(content)
