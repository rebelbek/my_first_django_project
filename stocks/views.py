import time as t
from datetime import datetime, time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Stocks
from .forms import SearchForm, DealForm
from .scripts.get_stocks import get_stocks_dict, get_stock_dict

# Create your views here.

stocks_fields_to_show = ['тикер', 'короткое название', 'полное название', 'количество акций', 'размер лота',
                         'цена 1 акции']


def auto_update():
    '''Автообновление акций каждые 60 секунд с 9:50 по 23:50'''
    duration = datetime.now().time() > time(9, 50) and datetime.now().time() < time(23, 50)
    while duration:
        stocks_fields_securities = get_stocks_dict(list(Stocks().__dict__.keys()))
        for item in stocks_fields_securities:
            try:
                Stocks.objects.filter(secid=item['secid']).update(**item)
            except:
                Stocks.objects.create(**item)
        t.sleep(60)  # модуль time as t


def stocks_update(request):
    auto_update()
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)


def stock_update(request, secid: str):
    stock_fields = get_stock_dict(dict(Stocks.objects.get(secid=secid).__dict__.items()))
    Stocks.objects.filter(secid=secid).update(**stock_fields)
    redirect_url = reverse('stock_detail', args=[secid])
    return HttpResponseRedirect(redirect_url)


def stocks_main(request):
    form = SearchForm()
    stocks = Stocks.objects.order_by('secid')
    stocks_count = stocks.count()
    context = {'stocks': stocks,
               'form': form,
               'stocks_count': stocks_count,
               'stocks_fields': stocks_fields_to_show,
               'current_time': datetime.now().time()}
    return render(request, 'stocks/stocks.html', context=context)


def stock_detail(request, secid: str):
    stock = get_object_or_404(Stocks, secid=secid)
    form = DealForm
    values_list = list(stock.__dict__.items())[2:]
    context = {'values_list': values_list,
               'stock': stock,
               'form': form}
    return render(request, 'stocks/stock_detail.html', context=context)


def stocks_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
            stocks = Stocks.objects.filter(Q(secid__icontains=form.cleaned_data['input']) |
                                           Q(shortname__icontains=form.cleaned_data['input']) |
                                           Q(secname__icontains=form.cleaned_data['input']))
    else:
        redirect_url = reverse('main_stocks')
        return HttpResponseRedirect(redirect_url)
    stocks_count = stocks.count()
    context = {'stocks': stocks,
               'form': form,
               'stocks_count': stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


@login_required
def stocks_delete(request):
    if request.user.is_superuser:
        with (connection.cursor() as cursor):
            cursor.execute("delete from stocks_stocks")
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)


@login_required
def stocks_download(request):
    if request.user.is_superuser:
        stocks_fields_securities = get_stocks_dict(dict(Stocks().__dict__.items()))
        for item in stocks_fields_securities:
            Stocks.objects.create(**item)
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)
