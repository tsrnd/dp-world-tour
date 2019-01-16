from django.core import validators
from rest_framework import serializers

class ListStadium(serializers.Serializer):
    time_from = serializers.IntegerField(required=False, validators=[validators.integer_validator])
    time_to = serializers.IntegerField(required=False)
    price = serializers.IntegerField(required=False)
