from django.db import models

# Create your models here.

class Circuit (models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    land = models.CharField(max_length=30)


spa = Circuit.objects.create(name= "Spa-Francorchamps", land= "Belgium")