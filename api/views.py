from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CircuitSerializer, LapSerializer, FollowerListSerializer
from django.apps import apps
from .models import Circuit, Lap, FollowerList

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  def get_queryset(self):
    userId = self.request.query_params.get("id", None)
    if userId:
      return User.objects.filter(id=userId)
    return super().get_queryset()


class CircuitViewSet(viewsets.ModelViewSet):
  queryset = Circuit.objects.all()
  serializer_class = CircuitSerializer

class LapViewSet(viewsets.ModelViewSet):
  queryset = Lap.objects.all()
  serializer_class = LapSerializer

class FollowerListViewSet(viewsets.ModelViewSet):
  queryset = FollowerList.objects.all()
  serializer_class = FollowerListSerializer