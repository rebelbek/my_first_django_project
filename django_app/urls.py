from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_page, name = 'first'),
    path('<int:number>', views.detail, name='chapter'),
]