from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('cabinet', views.cabinet, name='cabinet'),
    ]