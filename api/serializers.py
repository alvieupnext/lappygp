from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.apps import apps

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'date_joined']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user

class CircuitSerializer(serializers.ModelSerializer):
  class Meta:
    model = apps.get_model('playground', 'circuit')
    fields = ['id', 'name', 'land', 'created_by', 'length', 'created_at']

  def create(self, validated_data):
    circuit = apps.get_model('playground', 'circuit').objects.create(**validated_data)
    return circuit

class LapSerializer(serializers.ModelSerializer):
  class Meta:
    model = apps.get_model('playground', 'lap')
    fields = ['id', 'time', 'circuit', 'user', 'weather', 'uploaded_on']

  def create(self, validated_data):
    lap = apps.get_model('playground', 'lap').objects.create(**validated_data)
    return lap