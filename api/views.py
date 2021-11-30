from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CircuitSerializer, LapSerializer, FollowerSerializer, UserProfileSerializer
from django.apps import apps
from .models import Circuit, Lap, UserProfile, UserFollowing
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import redirect

class UserProfileViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  def get_queryset(self):
    userId = self.request.query_params.get("user", None)
    if userId:
      return UserProfile.objects.filter(user=userId)
    return super().get_queryset()

  # @action(detail=True, methods=['put'])
  # def profile(self, request, pk=None):
  #   user = self.get_object()
  #   profile = user.profile
  #   serializer = UserProfileSerializer(profile, data=request.data)
  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.data, status=200)
  #   else:
  #     return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = User.objects.all()
  serializer_class = UserSerializer
  # def get_queryset(self):
  #   userId = self.request.query_params.get("id", None)
  #   if userId:
  #     return User.objects.filter(id=userId)
  #   return super().get_queryset()


class CircuitViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Circuit.objects.all()
  serializer_class = CircuitSerializer

class LapViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Lap.objects.all()
  serializer_class = LapSerializer

class FollowerViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = UserFollowing.objects.all()
  serializer_class = FollowerSerializer