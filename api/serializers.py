from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Circuit, Lap, UserProfile, UserFollowing
import requests
import json
from geopy.geocoders import Nominatim

#get from the Nominatim API coordinates
def getCoordinates(name):
  loc = Nominatim(user_agent="GetLoc")
  getLoc = loc.geocode(name)
  return getLoc.latitude, getLoc.longitude

# upload user-generated lap times to a third-party database
# All other lap times can be found here: 'https://lappygp-5ce5.restdb.io/rest/laptimes' Use the same headers
def uploadLap(lap):
  # get all the needed info for the database
  time = str(lap.time)
  circt = lap.circuit.name
  use = lap.user.username
  weather = lap.weather
  # Link to the third party database
  url = 'https://lappygp-5ce5.restdb.io/rest/laptimes'
  # prepare the data we want to send to the database
  payload = json.dumps({'time': time, 'circuit': circt, 'user': use, 'weather': weather})
  #needed headers
  headers = {
    'content-type': "application/json",
    'x-apikey': "4fe444bd127698e1012e7fcddd3508d7becd3",
    'cache-control': "no-cache"
  }
  #send a POST request to the API
  response = requests.request("POST", url, data=payload, headers=headers)


# Serializer for the UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user', 'avatar']

  # only update if the user information belongs to the user who requested the information
  def update(self, instance, validated_data):
    user = self.context['request'].user
    if user.pk != instance.user.id:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    instance.avatar = validated_data['avatar']
    instance.save()
    return instance

# Serializer for the users
class UserSerializer(serializers.ModelSerializer):
  # Uncomment this to get all the info from the corresponding userprofile in the same query call
  # userprofile = UserProfileSerializer()
  class Meta:
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'date_joined', 'userprofile']
    # password protection
    extra_kwargs = {'password': {'write_only': True, 'required': True}, 'userprofile': {'required': False}}

  def create(self, validated_data):
    # create users with all the data you validated
    user = User.objects.create_user(**validated_data)
    #assign them a new token for authentication
    Token.objects.create(user=user)
    #assign them a default photo as avatar
    defaultPhoto = 'images/unknown.png'
    UserProfile.objects.create(user= user, avatar = defaultPhoto)
    return user

  def update(self, instance, validated_data):
    #get information from the current user requesting
    user = self.context['request'].user

    #reject the update if the user information isn't from the user who sent the request
    if user.pk != instance.pk:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

    #else update what is needed
    instance.username = validated_data['username']
    instance.email = validated_data['email']
    instance.password = validated_data['password']

    #save changes
    instance.save()
    return instance


class CircuitSerializer(serializers.ModelSerializer):
  # Uncomment to get all the info from the creator in the same query call
  # created_by = UserSerializer()
  class Meta:
    model = Circuit
    fields = ['id', 'name',  'created_by', 'created_at', 'longitude', 'latitude']
    #allow longitude and latitude to be optional (so our API can fill these correctly in
    extra_kwargs = {'longitude': {'required': False}, 'latitude': {'required': False}}

  def create(self, validated_data):
    #get name from our data
    name = validated_data['name']
    #get the coordinates
    lat, long = getCoordinates(name)
    #create circuit using user-given data
    circuit = Circuit.objects.create(**validated_data)
    #save longitude and latitude on the object
    circuit.longitude = long
    circuit.latitude = lat
    #save changes
    circuit.save()
    return circuit

class LapSerializer(serializers.ModelSerializer):
  # Uncomment to get all the info from the user and the circuit in the same query call
  # user = UserSerializer()
  # circuit = CircuitSerializer()
  class Meta:
    model = Lap
    fields = ['id', 'time', 'circuit', 'user', 'weather', 'uploaded_on']

  def create(self, validated_data):
    #create a lap object
    lap = Lap.objects.create(**validated_data)
    #upload it to the third-party API
    uploadLap(lap)
    return lap


  def update(self, instance, validated_data):
    # only update if the lap belongs to the user who requested the information
    user = self.context['request'].user
    if user != instance.user.id:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    # allow weather updates
    instance.weather = validated_data['weather']
    #save changes
    instance.save()
    return instance


class FollowerSerializer(serializers.ModelSerializer):
  # Uncomment to get all the info from the follower and the followed in the same query call
  # user = UserSerializer()
  # followed = UserSerializer()
  class Meta:
    model = UserFollowing
    fields = ['id', 'user', 'followed', 'date']

  def create(self, validated_data):
    # only create follow action if the user corresponds
    user = self.context['request'].user
    if user.pk != validated_data['user'].pk:
      raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
    follow = UserFollowing.objects.create(**validated_data)
    return follow