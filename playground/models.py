from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Circuit (models.Model):
    name = models.CharField(max_length=30)
    land = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.fields.IntegerField()

# class Lap(models.Model):


# adds a circuitobject
# spa = Circuit.objects.create(name= "Spa-Francorchamps", land= "Belgium")