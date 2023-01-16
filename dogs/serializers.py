from rest_framework import serializers
from .models import DogPic


class DogPicSerializer(serializers.ModelSerializer):
    original = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()

    class Meta:
        model = DogPic
        fields = ['original','modified','metadata']
    def get_original(self,dogPic):
        url = dogPic.original.url
        return url
    def get_modified(self,dogPic):
        url = dogPic.modified.url
        return url