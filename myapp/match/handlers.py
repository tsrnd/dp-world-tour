import inject
import json
import logging
from rest_framework.generics import GenericAPIView
from shared.base_handler import *
from myapp.match.requests import FindMatchSerializer
from rest_framework.permissions import IsAuthenticated
from myapp.permission.match_permission import IsLeadTeam
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
        context = {
            "message": "Create find match successful"
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )
