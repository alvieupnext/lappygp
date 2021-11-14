from . import views
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView
from django.urls import path

# Create your views here
# .
urlpatterns = [
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login"),
    path('register/',views.registerView,name="register"),
    path('change_password/', views.MyPasswordChangeView.as_view(), name="change_password"),
    path('change_password/done/', views.MyPasswordResetDoneView.as_view(), name='password_change_done'),
    path('logout/',LogoutView.as_view(next_page='dashboard'),name="logout"),
]