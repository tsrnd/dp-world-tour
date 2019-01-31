from rest_framework import serializers

from myapp.models.stadium_registers import StadiumRegister
from django.shortcuts import get_object_or_404
from myapp.models.stadiums import Stadium
from shared import utils
from rest_framework.serializers import (
        ModelSerializer,
        ValidationError,
    )


class BookingStadiumSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    stadium = serializers.IntegerField(required=False)

    def get_total_price(self, time_from, time_to, stadium_id):
        return StadiumRegister.custom_objects.get_total_price(time_from, time_to, stadium_id)
    class Meta:
        model = StadiumRegister
        fields = ('time_from', 'time_to', 'total_price', 'stadium')

    def validate(self, data):
        if not StadiumRegister.custom_objects.is_ready(data['time_from'], data['time_to'], data['stadium']):
            raise serializers.ValidationError({'stadium_id': 'Not ready'})

        if data['time_from'] >= data['time_to']:
            raise serializers.ValidationError({'time_from': 'Must be larger than time_to'})
        
        return data

    def create(self, validated_data):
        stadium_register = StadiumRegister.objects.create(
            time_from=validated_data['time_from'],
            time_to=validated_data['time_to'],
            stadium_id=validated_data['stadium'],
            user_id = self.context['request'].user.id,
            total_price=StadiumRegister.custom_objects.get_total_price(
                validated_data['time_from'],
                validated_data['time_to'],
                validated_data['stadium'],
            ),
        )
        return stadium_register

class BookingCancelSerializer(ModelSerializer):
    class Meta:
        model = StadiumRegister
        fields = ['id', 'status']
    
    def validate(self, data):
        if self.instance.user.id != self.context['request'].user.id:
            raise ValidationError({"permission": "This booking's request is not your booking request"})
        
        # check current booking request is pending
        if self.instance.status != 'PENDING':
            raise ValidationError({"status": "This booking's request is not pending"})
        return data
