from rest_framework import serializers


class FindMatchSerializer(serializers.Serializer):
    user_name = serializers.IntegerField(max_length=10)
