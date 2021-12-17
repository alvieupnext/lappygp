from django.db import models
from django.contrib.auth.models import User

# We are using the default Django User model for our users

class UserProfile(models.Model):
    # corresponds to just one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # saves a profile picture
    avatar = models.ImageField(upload_to='images')

#tracks when an user has followed another user
class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    date = models.DateTimeField(auto_now_add=True)

#circuit representation
class Circuit (models.Model):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(max_length=40, blank=True, default = 0)
    longitude = models.FloatField(max_length=40, blank=True, default = 0)

#lap representation
class Lap(models.Model):
    WEATHER_TYPES = (
        ('R', 'Rainy'),
        ('S', 'Sunny'),
        ('C', 'Cloudy')
    )
    time = models.CharField(max_length=30)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weather= models.CharField(max_length=1, choices=WEATHER_TYPES)
    uploaded_on = models.DateTimeField(auto_now_add=True)