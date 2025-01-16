from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('deal-detail/<int:id>', views.deal_detail, name='deal_detail'),
    path('deal-add/<str:secid>', views.deal_add, name='deal_add'),
    path('stocks-add/<int:id>', views.stocks_add, name='stocks_add'),
    path('deal-delete/<int:id>', views.deal_delete, name='deal_delete'),
    path('check-border', views.check_border, name='check_border'),
    path('notifications', views.notifications, name='notifications'),
    path('notifications-delete', views.notifications_delete, name='notifications_delete'),
    path('notification-delete/<int:id>', views.notification_delete, name='notification_delete'),
    path('notification-read/<int:id>', views.notification_read, name='notification_read'),
    ]