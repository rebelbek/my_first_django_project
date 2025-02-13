import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Stocks
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
    else:
        stocks = Stocks.objects.all()
    stocks_count = stocks.count()
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
    stocks = Stocks.objects.order_by(filter_field)
    return render(request, 'stocks/partial_stock_list.html', {'stocks': stocks})


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
        Stocks.download()
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)


def stock_update(request, secid: str):
    Stocks.update_one(secid=secid)
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)
