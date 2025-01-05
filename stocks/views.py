from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StockInfo
from .forms import SearchForm
from .scripts.get_stocks import get_stocks_list

# Create your views here.

def stocks_main(request):
    form = SearchForm()
    stocks = StockInfo.objects.all()
    stocks_count = stocks.count()
    stocks_fields = ['secid', 'boardid', 'shortname', 'lotsize', 'secname', 'listlevel', 'issuesize']
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_fields': stocks_fields}
    return render(request, 'stocks/stocks.html', context=context)


def stocks_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['field'] == 'Secname':
            stocks = StockInfo.objects.filter(secname__icontains=form.cleaned_data['input'])
        elif form.cleaned_data['field'] == 'Secid':
            stocks = StockInfo.objects.filter(secid__icontains=form.cleaned_data['input'])
    else:
        redirect_url = reverse('main_stocks')
        return HttpResponseRedirect(redirect_url)
    stocks_count = stocks.count()
    stocks_keys = list(StockInfo().__dict__.keys())[1:]
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_keys': stocks_keys}
    return render(request, 'stocks/stocks.html', context=context)


def stocks_update(request):
    stocks_list = get_stocks_list()
    StockInfo.objects.all().delete()
    for item in stocks_list:
        stock = StockInfo(*item)
        stock.save()
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)