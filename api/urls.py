from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet, CircuitViewSet, LapViewSet




router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('circuits', CircuitViewSet)
router.register('laps', LapViewSet)

urlpatterns = [
  path('', include(router.urls))
]