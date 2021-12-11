from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.apps import apps
from PIL import Image
from .models import Circuit, Lap, UserProfile, UserFollowing
from rest_framework.permissions import IsAuthenticated
import requests
import json
from geopy.geocoders import Nominatim

def getCoordinates(name):
  loc = Nominatim(user_agent="GetLoc")
  getLoc = loc.geocode(name)
  return getLoc.latitude, getLoc.longitude

# upload user-generated lap times to a third-party database
def uploadLap(lap):
  # get all the needed info for the database
  time = str(lap.time)
  print(time)
  circt = lap.circuit.name
  use = lap.user.username
  weather = lap.weather
  # Link to the third party database
  url = 'https://lappygp-5ce5.restdb.io/rest/laptimes'
  # prepare the data we want to send to the database
  payload = json.dumps({'time': time, 'circuit': circt, 'user': use, 'weather': weather })
  #needed headers
  headers = {
    'content-type': "application/json",
    'x-apikey': "4fe444bd127698e1012e7fcddd3508d7becd3",
    'cache-control': "no-cache"
  }
  response = requests.request("POST", url, data=payload, headers=headers)
  print(response.text)



class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['avatar']

class UserSerializer(serializers.ModelSerializer):
  userprofile = UserProfileSerializer()

  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'date_joined', 'userprofile']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    photo = 'images/unknown.png'
    Token.objects.create(user=user)
    UserProfile.objects.create(user= user, avatar = photo)
    return user

  def update(self, instance, validated_data):
    user = self.context['request'].user

    if user.pk != instance.pk:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

    instance.username = validated_data['username']
    instance.email = validated_data['email']
    instance.password = validated_data['password']

    instance.save()
    return instance

  def update(self, instance, validated_data):
    user = self.context['request'].user
    if user.pk != instance.user.id:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    instance.avatar = validated_data['avatar']
    instance.save()
    return instance


class CircuitSerializer(serializers.ModelSerializer):
  # created_by = UserSerializer()
  class Meta:
    model = Circuit
    fields = ['id', 'name', 'land', 'created_by', 'created_at', 'longitude', 'latitude']
    extra_kwargs = {'longitude': {'required': False}, 'latitude': {'required': False}}

  def create(self, validated_data):
    name = validated_data['name']
    long, lat = getCoordinates(name)
    circuit = Circuit.objects.create(**validated_data)
    circuit.longitude = long
    circuit.latitude = lat
    circuit.save()
    return circuit

class LapSerializer(serializers.ModelSerializer):
  # user = UserSerializer()
  # circuit = CircuitSerializer()
  class Meta:
    model = Lap
    fields = ['id', 'time', 'circuit', 'user', 'weather', 'uploaded_on']

  def create(self, validated_data):
    lap = Lap.objects.create(**validated_data)
    uploadLap(lap)
    return lap

  def update(self, instance, validated_data):
    user = self.context['request'].user
    if user != instance.user.id:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    instance.weather = validated_data['weather']
    instance.save()
    return instance


class FollowerSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  followed = UserSerializer()
  class Meta:
    model = UserFollowing
    fields = ['id', 'user', 'followed', 'date']

  def create(self, validated_data):
    user = self.context['request'].user
    if user.pk != validated_data['user'].pk:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    follow = UserFollowing.objects.create(**validated_data)
    return follow




  # def update(self, instance, validated_data):
  #   user = self.context['request'].user
  #   if user.pk != instance.user.pk:
  #     raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
  #   instance.followers += validated_data['followers']
  #   instance.follows += validated_data['follows']