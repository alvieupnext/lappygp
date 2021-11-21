from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.apps import apps
from .models import Circuit, Lap, FollowerList

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'date_joined']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    FollowerList.objects.create(user = user)
    return user

class CircuitSerializer(serializers.ModelSerializer):
  class Meta:
    model = Circuit
    fields = ['id', 'name', 'land', 'created_by', 'length', 'created_at']

  def create(self, validated_data):
    circuit = Circuit.objects.create(**validated_data)
    return circuit

class LapSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lap
    fields = ['id', 'time', 'circuit', 'user', 'weather', 'uploaded_on']

  def create(self, validated_data):
    lap = Lap.objects.create(**validated_data)
    return lap

class FollowerListSerializer(serializers.ModelSerializer):
  class Meta:
    model = FollowerList
    fields = ['user', 'followers', 'follows']