from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images')

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    date = models.DateTimeField(auto_now_add=True)

class Circuit (models.Model):
    name = models.CharField(max_length=30)
    land = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(max_length=40, blank=True, default = 0)
    longitude = models.FloatField(max_length=40, blank=True, default = 0)

class Lap(models.Model):
    WEATHER_TYPES = (
        ('R', 'Rainy'),
        ('S', 'Sunny'),
        ('C', 'Cloudy')
    )
    time = models.TimeField()
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weather= models.CharField(max_length=1, choices=WEATHER_TYPES)
    uploaded_on = models.DateTimeField(auto_now_add=True)