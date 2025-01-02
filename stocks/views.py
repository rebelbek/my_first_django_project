from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StockInfo
from . import get_stocks

# Create your views here.

def main_stocks(request):
    stocks = StockInfo.objects.all()
    stocks_count = stocks.count()
    stocks_keys = list(StockInfo().__dict__.keys())[1:]
    context = {'stocks' : stocks,
               'stocks_count' : stocks_count,
               'stocks_keys': stocks_keys}
    return render(request, 'stocks/stocks.html', context=context)


def update_stocks(request):
    stocks_list = get_stocks.get_stocks_list()
    StockInfo.objects.all().delete()
    for item in stocks_list:
        stock = StockInfo(*list(item.values()))
        stock.save()
    redirect_url = reverse('main_stocks')
    return HttpResponseRedirect(redirect_url)


def delete_stocks(request):
    StockInfo.objects.all().delete()
    redirect_url = reverse('main_stocks')
    return HttpResponseRedirect(redirect_url)