from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_stocks, name = 'main_stocks'),
    path('update-stocks', views.update_stocks),
    path('delete-stocks', views.delete_stocks),
]