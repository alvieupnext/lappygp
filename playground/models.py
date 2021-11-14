from django.db import models

# Create your models here.

class Circuit (models.Model):
    name = models.CharField(max_length=30)
    land = models.CharField(max_length=30)

# adds a circuitobject
# spa = Circuit.objects.create(name= "Spa-Francorchamps", land= "Belgium")