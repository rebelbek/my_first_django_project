from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    path('send-email-to-verify', views.send_email_to_verify, name='send_email_to_verify'),
    path('send-email-to-verify/done', views.send_email_to_verify_done, name='send_email_to_verify_done'),
    path('check-borders', views.check_borders, name='check_borders'),
    path('deal-detail/<int:pk>', views.deal_detail, name='deal_detail'),
    path('deal-add/<str:secid>', views.deal_add, name='deal_add'),
    path('stocks-add/<int:pk>', views.stocks_add, name='stocks_add'),
    path('deal-delete/<int:pk>', views.deal_delete, name='deal_delete'),
    path('reports', views.reports, name='reports'),
    path('get-reports/<str:model>/<str:format_file>', views.get_reports, name='get_reports'),
    ]