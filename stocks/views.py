import time as t
from datetime import datetime, time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from .models import Stocks
from .forms import SearchForm, StockInfoForm
from .scripts.get_stocks import get_stocks_dict, get_stock_dict

# Create your views here.

stocks_fields_to_show = ['тикер', 'короткое название', 'полное название', 'количество акций', 'размер лота',
                         'цена 1 акции']


def auto_update():
    '''Автообновление акций каждые 10 секунд с 9:50 по 23:50'''
    duration = datetime.now().time() > time(9, 50) and datetime.now().time() < time(23, 50)
    while duration:
        stocks_fields_securities = get_stocks_dict(dict(Stocks().__dict__.items()))

        for item in stocks_fields_securities:
            try:
                Stocks.objects.filter(secid=item['secid']).update(**item)
            except:
                Stocks.objects.create(**item)

        t.sleep(10)  # модуль time as t


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
    if request.method == 'POST':
        form = StockInfoForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'stock_detail', args=[secid])
            return HttpResponseRedirect(redirect_url)
    else:
        form = StockInfoForm(instance=stock)
    values_list = list(stock.__dict__.items())[1:]
    context = {'values_list': values_list,
               'stock': stock,
               'form': form}
    return render(request, 'stocks/stock_detail.html', context=context)


def stocks_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['field'] == 'Secname':
            stocks = Stocks.objects.filter(secname__icontains=form.cleaned_data['input'])
        elif form.cleaned_data['field'] == 'Secid':
            stocks = Stocks.objects.filter(secid__icontains=form.cleaned_data['input'])
    else:
        redirect_url = reverse('main_stocks')
        return HttpResponseRedirect(redirect_url)
    stocks_count = stocks.count()
    context = {'stocks': stocks,
               'form': form,
               'stocks_count': stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


def stocks_update(request):
    # stocks_fields_securities = get_stocks_dict(dict(StockInfoSecurities().__dict__.items()))
    # stocks_fields_marketdata = get_stocks_dict(dict(StockInfoMarketdata().__dict__.items()))
    # # обновить данные для таблицы StockInfoSecurities
    # unchangeable_stocks = [item.secid for item in StockInfoSecurities.objects.all() if item.unchangeable is True]
    # for item in stocks_fields_securities:
    #     if item['secid'] not in unchangeable_stocks:
    #         try:
    #             StockInfoSecurities.objects.filter(secid=item['secid']).update(**item)
    #         except:
    #             StockInfoSecurities.objects.create(**item)
    #     else:
    #         del item['shortname']
    #         del item['secname']
    #         StockInfoSecurities.objects.filter(secid=item['secid']).update(**item)
    # # обновить данные для таблицы StockInfoMarketdata
    # for item in stocks_fields_marketdata:
    #     try:
    #         StockInfoMarketdata.objects.filter(secid=item['secid']).update(**item)
    #     except:
    #         StockInfoMarketdata.objects.create(**item)
    # # связать таблицы у новых акций
    # new_stocks = [item for item in StockInfoSecurities.objects.all() if not item.marketdata]
    # if new_stocks:
    #     for item in new_stocks:
    #         item.marketdata = StockInfoMarketdata.objects.get(secid=f'{item.secid}')
    #         item.save()
    auto_update()
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)


def stock_update(request, secid: str):
    stock_fields_securities = get_stock_dict(dict(Stocks.objects.get(secid=secid).__dict__.items()))
    Stocks.objects.filter(secid=secid).update(**stock_fields_securities)
    redirect_url = reverse('stock_detail', args=[secid])
    return HttpResponseRedirect(redirect_url)


def stocks_delete(request):
    with (connection.cursor() as cursor):
        cursor.execute("delete from stocks_stocks")
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)


def stocks_download(request):
    stocks_fields_securities = get_stocks_dict(dict(Stocks().__dict__.items()))
    for item in stocks_fields_securities:
        Stocks.objects.create(**item)
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)
