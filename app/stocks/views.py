import datetime
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Stocks, CronLogs
from .forms import SearchForm, DealForm

# Create your views here.

offset = datetime.timezone(datetime.timedelta(hours=3))
stocks_fields_to_show = {'тикер': 'secid', 'короткое название': 'shortname', 'полное название':
    'secname', 'кол-во акций': 'issuesize', 'размер лота': 'lotsize', 'цена 1 акции': 'last'}


def stocks_main(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        stocks = Stocks.objects.filter(Q(secid__icontains=form.cleaned_data['input']) |
                                       Q(shortname__icontains=form.cleaned_data['input']) |
                                       Q(secname__icontains=form.cleaned_data['input']))
        stocks_count = stocks.count()
    else:
        stocks = cache.get_or_set('cached_stocks', Stocks.objects.all(), 60)
        stocks_count = cache.get_or_set('cached_count', stocks.count(), 60)
    date_moscow = datetime.datetime.now(offset)
    context = {'stocks': stocks,
               'form': form,
               'stocks_count': stocks_count,
               'stocks_fields': stocks_fields_to_show.keys(),
               'msc_time': date_moscow}
    return render(request, 'stocks/stocks.html', context=context)


def stock_detail(request, secid: str):
    stock = get_object_or_404(Stocks, secid=secid)
    values_list = list(stock.__dict__.items())[2:]
    if request.htmx:
        return HttpResponse(''.join([f'<tr><td><b>{key.title()}</b></td><td><b>{value}</b></td></tr>'
                            for key, value in values_list]))
    form = DealForm
    context = {'values_list': values_list,
               'stock': stock,
               'form': form}
    return render(request, 'stocks/stock_detail.html', context=context)


def stock_list_sort(request, filter_field, direction):
    filter_field = stocks_fields_to_show[f'{filter_field}']
    if direction == 'descend':
        filter_field = '-' + filter_field
    cache_key = 'cached_sort_stocks_' + filter_field
    stocks = cache.get_or_set(cache_key, Stocks.objects.order_by(filter_field), 60)
    return render(request, 'stocks/partial_stock_list.html', {'stocks': stocks})


@login_required
def stocks_delete(request):
    if request.user.is_superuser:
        with (connection.cursor() as cursor):
            cursor.execute("delete from stocks_stocks")
        cache.delete('cached_stocks')
        cache.delete('stocks_count')
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)


@login_required
def stocks_download(request):
    if request.user.is_superuser:
        Stocks.download()
        cache.delete('cached_stocks')
        cache.delete('stocks_count')
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)


def stocks_update(request):
    if request.user.is_superuser:
        Stocks.update_all()
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)


def stock_update(request, secid: str):
    Stocks.update_one(secid=secid)
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)


def show_update_logs(request):
    logs = CronLogs.objects.all()[:20]
    context = {'logs': logs}
    return render(request, 'stocks/logs.html', context=context)
