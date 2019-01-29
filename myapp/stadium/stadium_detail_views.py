from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from myapp.models.stadiums import Stadium
from myapp.serializer.stadium_serializer import StadiumSerializer


class StadiumDetailView(APIView):

    def get(self, request, stadiumID):
        stadium = get_object_or_404(Stadium, pk=stadiumID)
        serializer = StadiumSerializer(stadium)
        return Response(serializer.data, status=status.HTTP_200_OK)
