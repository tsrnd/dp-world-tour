from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .booking_serializer import BookingStadiumSerializer

from django.http import HttpResponse, HttpResponseNotFound


class BookingView(APIView):

    def post(self, request, pk):
        requestPost = request.POST
        name = requestPost.get('name')
        print(name)
        location = requestPost.get('location')
        print(location)
        phone_number = requestPost.get('phone_number')
        print(phone_number)
        bank_number = requestPost.get('bank_number')
        print(bank_number)
        status = requestPost.get('status')
        print(status)
        print("request={}".format(request))
        print("request.POST={}".format(request.POST))
        print("pk={}".format(pk))
        # stadium = get_object_or_404()
        data = {'response': 'vanlam1502'}
        return Response(data)

# {
#       "name": "string",
#       "location": "string",
#       "phone_number": "string",
#       "email": "string",
#       "price": "string",
#       "bank_number": "string",
#       "status": "pending"
#     }
