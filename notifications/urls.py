from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('notifications-delete', views.notifications_delete, name='notifications_delete'),
    path('notification-delete/<int:id>', views.notification_delete, name='notification_delete'),
    path('notifications-read', views.notifications_read, name='notifications_read'),
    ]