from django.core import validators
from rest_framework import serializers

class ListStadiumSerializer(serializers.Serializer):
    time_from = serializers.IntegerField(required=True)
    time_to = serializers.IntegerField(required=True)
    max_price = serializers.IntegerField(required=False)
    min_price = serializers.IntegerField(required=False)
    result_limit = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)

class ListStadiumResponse(object):
    def __init__(self, id, name, lat, lng, phone_number, email, price, bank_number):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.phone_number = phone_number
        self.email = email
        self.price = price
        self.bank_number = bank_number
