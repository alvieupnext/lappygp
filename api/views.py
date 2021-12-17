from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, CircuitSerializer, LapSerializer, FollowerSerializer, UserProfileSerializer
from .models import Circuit, Lap, UserProfile, UserFollowing
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import wikipediaapi
import json

#For all the ViewSets is the following true: You can only POST to the API if you're authenticated, if you're not you can only see the contents
class UserProfileViewSet(viewsets.ModelViewSet):
  #enforce the permission
  permission_classes = (IsAuthenticatedOrReadOnly,)
  #establish the queryset
  queryset = UserProfile.objects.all()
  #use our serializer for lay-out and handling create, update and delete
  serializer_class = UserProfileSerializer
  #adding the ability to take query parameters
  # def get_queryset(self):
  #   userId = self.request.query_params.get("username", None)
  #   print(userId)
  #   if userId:
  #     return UserProfile.objects.filter(username=userId)
  #   return super().get_queryset()


def getInfoFromWikipedia(name):
  #get the wikipedia pages in english
  wiki_wiki = wikipediaapi.Wikipedia('en')
  #search for the page
  page = wiki_wiki.page(name)
  #if found, return title, summary and link as a json
  if page.exists():
    data = {"title": page.title, "summary": page.summary, "link": page.fullurl}
    return HttpResponse(content=json.dumps(data), content_type='application/json')
  #else throw a 400 error
  return HttpResponse('<h1>Wiki Not Found</h1>', status=408)

#able to bypass csrf
@csrf_exempt
def WikiView(request):
  #front-end can request wikipedia information using POST
  if request.method == "POST":
    name = request.POST['circuit_name']
    return getInfoFromWikipedia(name)

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  def get_queryset(self):
    userId = self.request.query_params.get("username", None)
    if userId:
      return User.objects.filter(username=userId)
    return super().get_queryset()


class CircuitViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Circuit.objects.all()
  serializer_class = CircuitSerializer
  def get_queryset(self):
    name = self.request.query_params.get("name", None)
    if name:
      return Circuit.objects.filter(name=name)
    return super().get_queryset()

class LapViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Lap.objects.all()
  serializer_class = LapSerializer
  def get_queryset(self):
    user = self.request.query_params.get("user", None)
    circuit = self.request.query_params.get("circuit", None)
    result = Lap.objects.all()
    if user:
      result = result.filter(user=user)
    if circuit:
      result = result.filter(circuit=circuit)
    return result

class FollowerViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = UserFollowing.objects.all()
  serializer_class = FollowerSerializer
  def get_queryset(self):
    user = self.request.query_params.get("user", None)
    by = self.request.query_params.get("by", None)
    result = UserFollowing.objects.all()
    if user:
      result = result.filter(followed=user)
    if by:
      result = result.filter(user=by)
    return result