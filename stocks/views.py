from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StockInfoSecurities, StockInfoMarketdata
from .forms import SearchForm, StockInfoForm
from .scripts.get_stocks import get_stocks_dict, get_stock_dict

# Create your views here.

stocks_fields_to_show = ['тикер', 'короткое название', 'полное название', 'количество акций', 'размер лота', 'цена 1 акции']


def stocks_main(request):
    form = SearchForm()
    stocks = StockInfoSecurities.objects.order_by('secid')
    stocks_count = stocks.count()
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


def stock_detail(request, secid: str):
    stock = get_object_or_404(StockInfoSecurities, secid=secid)
    if request.method == 'POST':
        form = StockInfoForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'stock_detail', args=[secid])
            return HttpResponseRedirect(redirect_url)
    else:
        form = StockInfoForm(instance=stock)
    values_list = list(stock.__dict__.items())[1:]
    try:
        stock_marketdata = StockInfoMarketdata.objects.get(secid=f'{stock.secid}')
        values_marketdata_list = list(stock_marketdata.__dict__.items())[4:]
    except:
        values_marketdata_list = []
    context = {'values_list' : values_list,
               'values_marketdata_list' : values_marketdata_list,
               'stock' : stock,
               'form' : form}
    return render(request, 'stocks/stock_detail.html', context=context)


def stocks_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['field'] == 'Secname':
            stocks = StockInfoSecurities.objects.filter(secname__icontains=form.cleaned_data['input'])
        elif form.cleaned_data['field'] == 'Secid':
            stocks = StockInfoSecurities.objects.filter(secid__icontains=form.cleaned_data['input'])
    else:
        redirect_url = reverse('main_stocks')
        return HttpResponseRedirect(redirect_url)
    stocks_count = stocks.count()
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


def stocks_update(request):
    StockInfoSecurities.objects.exclude(unchangeable=True).delete()
    StockInfoMarketdata.objects.all().delete()
    stocks_fields_securities = get_stocks_dict(dict(StockInfoSecurities().__dict__.items()))
    stocks_fields_marketdata = get_stocks_dict(dict(StockInfoMarketdata().__dict__.items()))
    # сохранить данные для таблицы StockInfoSecurities
    unchangeable_stocks = [item.secid for item in StockInfoSecurities.objects.all()]
    for item in stocks_fields_securities:
        if item['secid'] not in unchangeable_stocks:
            stock = StockInfoSecurities(**item)
            stock.save()
        else:
            del item['shortname']
            del item['secname']
            StockInfoSecurities.objects.filter(secid=item['secid']).update(**item)
    # сохранить данные для таблицы StockInfoMarketdata
    for item in stocks_fields_marketdata:
        stock = StockInfoMarketdata(**item)
        stock.save()
    # связать таблицы
    for item in StockInfoSecurities.objects.all():
        item.marketdata = StockInfoMarketdata.objects.get(secid=f'{item.secid}')
        item.save()
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)


def stock_update(request, secid: str):
    stock_fields_securities = get_stock_dict(dict(StockInfoSecurities.objects.get(secid=secid).__dict__.items()))
    stock_fields_marketdata = get_stock_dict(dict(StockInfoMarketdata.objects.get(secid=secid).__dict__.items()))
    stock = StockInfoSecurities.objects.get(secid=secid)
    # обновить данные для таблицы StockInfoSecurities
    if stock.unchangeable is True:
        del stock_fields_securities['shortname']
        del stock_fields_securities['secname']
        StockInfoSecurities.objects.filter(secid=secid).update(**stock_fields_securities)
    else:
        StockInfoSecurities.objects.filter(secid=secid).update(**stock_fields_securities)
    # обновить данные для таблицы StockInfoMarketdata
    StockInfoMarketdata.objects.get(secid=secid).delete()
    StockInfoMarketdata.objects.create(**stock_fields_marketdata)
    # связать таблицы
    stock = StockInfoSecurities.objects.get(secid=secid)
    stock.marketdata = StockInfoMarketdata.objects.get(secid=secid)
    stock.save()
    redirect_url = reverse('stock_detail', args=[secid])
    return HttpResponseRedirect(redirect_url)
