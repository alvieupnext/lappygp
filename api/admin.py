from django.contrib import admin
from .models import Circuit, Lap, UserFollowing, UserProfile

# Register your models here.

admin.site.register(Circuit)
admin.site.register(Lap)
admin.site.register(UserFollowing)
admin.site.register(UserProfile)