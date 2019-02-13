import inject, json, logging

from shared.base_handler import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from myapp.stadium.booking_serializer import (
    BookingCancelSerializer
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.mixins import UpdateModelMixin
from myapp.models.stadium_registers import StadiumRegister

class BookingCancel(UpdateModelMixin, GenericAPIView):
    bh = inject.attr(BaseHandler)
    serializer_class = BookingCancelSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'
    queryset = StadiumRegister.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=kwargs, partial=True)
        response = self.bh.validate(serializer)
        if response is not None:
            return response
        serializer.save()
        context = {
            "message": "Update booking successfully"
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        kwargs['status'] = 'CANCEL'
        return self.update(request, *args, **kwargs)