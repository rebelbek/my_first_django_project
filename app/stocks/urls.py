from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocks_main, name='stocks_main'),
    path('stock_list_sort/<filter_field>/<direction>/', views.stock_list_sort, name='stock_list_sort'),
    path('stock-update/<str:secid>', views.stock_update, name='stock_update'),
    path('stocks-update', views.stocks_update, name='stocks_update'),
    path('stocks-download', views.stocks_download, name='stocks_download'),
    path('stocks-delete', views.stocks_delete, name='stocks_delete'),
    path('logs', views.show_update_logs, name='show_update_logs'),
    path('resume', views.get_resume, name='get_resume'),
    path('<str:secid>', views.stock_detail, name='stock_detail'),
]
