from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Stocks
from .forms import SearchForm, DealForm


# Create your views here.

stocks_fields_to_show = ['тикер', 'короткое название', 'полное название', 'количество акций', 'размер лота',
                         'цена 1 акции']


def stock_update(request, secid: str):
    Stocks.update_one(secid=secid)
    redirect_url = request.META.get('HTTP_REFERER')
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
        Stocks.download()
        redirect_url = reverse('stocks_main')
        return HttpResponseRedirect(redirect_url)



