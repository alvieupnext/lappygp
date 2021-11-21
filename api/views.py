from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CircuitSerializer, LapSerializer, FollowerListSerializer
from django.apps import apps

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class CircuitViewSet(viewsets.ModelViewSet):
  queryset = apps.get_model('playground', 'circuit').objects.all()
  serializer_class = CircuitSerializer

class LapViewSet(viewsets.ModelViewSet):
  queryset = apps.get_model('playground', 'lap').objects.all()
  serializer_class = LapSerializer

class FollowerListViewSet(viewsets.ModelViewSet):
  queryset = apps.get_model('playground', 'followerlist').objects.all()
  serializer_class = FollowerListSerializer