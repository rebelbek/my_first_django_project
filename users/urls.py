from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('deal-add', views.deal_add, name='deal_add'),
    path('deal-delete/<int:id>', views.deal_delete, name='deal_delete'),
    ]