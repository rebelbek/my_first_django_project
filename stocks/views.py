from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import StockInfo
from .forms import SearchForm, StockInfoForm
from .scripts.get_stocks import get_stocks_list

# Create your views here.
stocks_fields_to_show = ['тикер', 'короткое название', 'полное название', 'количество акций', 'размер лота', 'цена']

def stocks_main(request):
    form = SearchForm()
    stocks = StockInfo.objects.order_by('secid')
    stocks_count = stocks.count()
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


def stock_detail(request, secid: str):
    stock = get_object_or_404(StockInfo, secid = secid)
    if request.method == 'POST':
        form = StockInfoForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'stock_detail', args=[secid])
            return HttpResponseRedirect(redirect_url)
    else:
        form = StockInfoForm(instance=stock)
    values_list = list(stock.__dict__.items())[1:]
    context = {'values_list' : values_list,
               'stock' : stock,
               'form' : form}
    return render(request, 'stocks/stock_detail.html', context=context)

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
    context = {'stocks' : stocks,
               'form' : form,
               'stocks_count' : stocks_count,
               'stocks_fields': stocks_fields_to_show}
    return render(request, 'stocks/stocks.html', context=context)


def stocks_update(request):
    stocks_list = get_stocks_list()
    StockInfo.objects.all().delete()
    for item in stocks_list:
        stock = StockInfo(*item)
        stock.save()
    redirect_url = reverse('stocks_main')
    return HttpResponseRedirect(redirect_url)