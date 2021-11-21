from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Circuit (models.Model):
    name = models.CharField(max_length=30)
    land = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    length = models.fields.IntegerField(null= True, blank=True, default=0)

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



# adds a circuitobject
# spa = Circuit.objects.create(name= "Spa-Francorchamps", land= "Belgium")