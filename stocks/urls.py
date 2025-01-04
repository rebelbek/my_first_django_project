from django.urls import path
from . import views

urlpatterns = [
    path('', views.stocks_main, name = 'stocks_main'),
    path('stocks-search', views.stocks_search, name = 'stocks_search'),
    path('stocks-update', views.stocks_update),
]