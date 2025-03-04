from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('', include('django.contrib.auth.urls')),
    path('check-borders', views.check_borders, name='check_borders'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('deal-detail/<int:pk>', views.deal_detail, name='deal_detail'),
    path('deal-add/<str:secid>', views.deal_add, name='deal_add'),
    path('stocks-add/<int:pk>', views.stocks_add, name='stocks_add'),
    path('deal-delete/<int:pk>', views.deal_delete, name='deal_delete'),
    path('reports', views.reports, name='reports'),
    path('get-reports/<str:model>/<str:format_file>', views.get_reports, name='get_reports'),
    ]