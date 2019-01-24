from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister
from django.shortcuts import get_object_or_404
from myapp.models.stadiums import Stadium
from shared import utils


class BookingStadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumRegister
        fields = ('time_from', 'time_to', 'total_price', 'stadium', 'user')

    def __init__(self, timeFrom, timeTo, stadiumID, userID):
        stadium = get_object_or_404(Stadium, pk=stadiumID)
        totalPrice = self.totalPrice(timeFrom, timeTo, stadium.price)
        data = {
            'time_from': timeFrom,
            'time_to': timeTo,
            'total_price': totalPrice,
            'stadium': stadium.id,
            'user': userID,
        }
        super(BookingStadiumSerializer, self).__init__(data=data)

    def totalPrice(self, timeFrom, timeTo, pricePerHour):
        return (utils.convertStringToTimestamp(timeTo) -
                utils.convertStringToTimestamp(timeFrom))/3600*pricePerHour
