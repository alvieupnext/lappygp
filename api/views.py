from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CircuitSerializer, LapSerializer, FollowerSerializer, UserProfileSerializer
from .models import Circuit, Lap, UserProfile, UserFollowing
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import wikipediaapi
import json


class UserProfileViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  def get_queryset(self):
    userId = self.request.query_params.get("user", None)
    if userId:
      return UserProfile.objects.filter(user=userId)
    return super().get_queryset()


def getInfoFromWikipedia(name):
  wiki_wiki = wikipediaapi.Wikipedia('en')
  page = wiki_wiki.page(name)
  if page.exists():
    data = {"title": page.title, "summary": page.summary, "link": page.fullurl}
    return HttpResponse(content=json.dumps(data), content_type='application/json')
  return HttpResponse('<h1>Wiki Not Found</h1>', status=408)



@csrf_exempt
def WikiView(request):
  if request.method == "POST":
    name = request.POST['circuit_name']
    return getInfoFromWikipedia(name)
  return HttpResponse('<h1>Hello HttpResponse</h1>')

class UserViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = User.objects.all()
  serializer_class = UserSerializer


class CircuitViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Circuit.objects.all()
  serializer_class = CircuitSerializer

class LapViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Lap.objects.all()
  serializer_class = LapSerializer

class FollowerViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = UserFollowing.objects.all()
  serializer_class = FollowerSerializer