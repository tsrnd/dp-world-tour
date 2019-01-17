from rest_framework import serializers
from myapp.models.stadium_registers import StadiumRegister


class BookingStadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumRegister
        fields = '__all__'
