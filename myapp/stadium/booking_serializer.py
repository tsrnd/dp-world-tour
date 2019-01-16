from rest_framework import serializers
from myapp.models.stadiums import Stadium


class BookingStadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'
