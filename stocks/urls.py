from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocks_main, name='stocks_main'),
    path('stock_list_sort/<filter_field>/<direction>/', views.stock_list_sort, name='stock_list_sort'),
    path('stocks-search', views.stocks_search, name='stocks_search'),
    path('stock-update/<str:secid>', views.stock_update, name='stock_update'),
    path('stocks-download', views.stocks_download, name='stocks_download'),
    path('stocks-delete', views.stocks_delete, name='stocks_delete'),
    path('<str:secid>', views.stock_detail, name='stock_detail'),
]
