from django.contrib import admin
from .models import Circuit, Lap, FollowerList

# Register your models here.

admin.site.register(Circuit)
admin.site.register(Lap)
admin.site.register(FollowerList)