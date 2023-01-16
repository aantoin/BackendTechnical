from random import choice
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DogPic
from .serializers import DogPicSerializer

# Create your views here.


class BlackAndWhiteView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request, format=None):
    pks = DogPic.objects.values_list('id', flat=True)
    if len(pks) < 1:
      return Response({}, 204)
    random_pk = choice(pks)
    dogPic = DogPic.objects.get(pk=random_pk)
    dogPicSerializer = DogPicSerializer(dogPic)
    return Response(dogPicSerializer.data)
