import inject
import json
import logging
from rest_framework.generics import GenericAPIView
from shared.base_handler import *
from myapp.match.requests import FindMatchSerializer
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class FindMatchAPIView(GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = FindMatchSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        context = {
            "message": "Create request successfully"
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )
