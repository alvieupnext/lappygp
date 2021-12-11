from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet, CircuitViewSet, LapViewSet, FollowerViewSet, UserProfileViewSet, WikiView




router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('circuits', CircuitViewSet)
router.register('laps', LapViewSet)
router.register('follow', FollowerViewSet)
router.register('profiles', UserProfileViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('wiki', WikiView,name="wikipedia")
]