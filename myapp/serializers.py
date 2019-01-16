from rest_framework import serializers
from myapp.models.stadiums import Stadium


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('id', 'name', 'lat', 'lng', 'phone_number', 'email', 'bank_num', 'price', 'created_at', 'updated_at', 'deleted_at')
