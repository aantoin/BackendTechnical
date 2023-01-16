from django.shortcuts import render
from django.db.models import F
from rest_framework import mixins,viewsets,permissions,decorators
from rest_framework.response import Response
from .models import KeyValuePair
from .serializers import KeyValuePairSerializer

# Create your views here.
class KeyValuePairViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = KeyValuePair.objects.all()
    serializer_class = KeyValuePairSerializer
    permission_classes = [permissions.AllowAny]

    @decorators.action(methods=['post'],detail=False)
    def increment(self, request):
        key = request.data.get('key')
        result = self.get_queryset().filter(key=key).update(value=F('value')+1)
        return Response({'success':result>0},200 if result else 400)


