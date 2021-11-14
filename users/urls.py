from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path

# Create your views here
# .
urlpatterns = [
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login"),
    path('register/',views.registerView,name="register"),
    path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
]