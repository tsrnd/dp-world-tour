import inject
import json
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from shared.base_handler import *
from myapp.match.requests import (
    FindMatchSerializer,
    MatchAcceptSerializer,
)
from myapp.models.matches import (
    Match,
)
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
