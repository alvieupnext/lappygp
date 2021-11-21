from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet, CircuitViewSet




router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('circuits', CircuitViewSet)

urlpatterns = [
  path('', include(router.urls))
]