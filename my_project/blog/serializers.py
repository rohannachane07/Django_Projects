# serializers.py

from rest_framework import serializers

class UserMessageSerializer(serializers.Serializer):
    user_message = serializers.CharField(max_length=255)
