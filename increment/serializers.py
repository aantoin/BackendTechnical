from rest_framework import serializers
from .models import KeyValuePair


class KeyValuePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValuePair
        fields = ['id','key','value']