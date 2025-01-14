from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F, Value, Avg, Sum
from datetime import date
from .forms import DealForm, DealInfoForm, AddStocksForm
from .models import UserDealInfo
from stocks.models import StockInfoSecurities, StockInfoMarketdata


# Create your views here.

deals_fields_to_show = ['тикер', 'дата сделки', 'полное название', 'кол-во акций', 'цена покупки',
                        'потрачено', 'цена текущая', 'стоимость', 'прибыль', 'X']

@login_required
def deal_add(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            stock = StockInfoSecurities.objects.get(secid=cd['secid'].upper())
            deal = UserDealInfo(stock=stock,
                                username=request.user.username,
                                secid=cd['secid'].upper(),
                                custom_secname = stock.secname,
                                quantity=cd['quantity'],
                                buy_price=cd['buy_price'],
                                date=date.today())
            deal.save()
    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


@login_required
def stocks_add(request, id: int):
    deal = get_object_or_404(UserDealInfo, id=id)
    if request.method == 'POST':
        form = AddStocksForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            deal.quantity += cd['quantity']
            deal.buy_price = (((deal.buy_price * deal.quantity) +
                                (cd['buy_price'] * cd['quantity'])) /
                                (deal.quantity + cd['quantity']))
            deal.save()
    redirect_url = reverse('deal_detail', args=[id])
    return HttpResponseRedirect(redirect_url)


@login_required
def deal_delete(request, id: int):
    deal = UserDealInfo.objects.get(id=id)
    if deal.username == request.user.username:
        deal.delete()
    else:
        raise Http404
    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


@login_required
def cabinet(request):
    form = DealForm()
    deals = UserDealInfo.objects.filter(username=request.user.username).annotate(
        cost=F('quantity') * F('buy_price'),
        value=F('quantity') * F('stock__marketdata__last'),
        profit=F('value') - F('cost'),
    )
    agg = deals.aggregate(Sum('cost'), Sum('value'), Sum('profit'))
    context = {'form': form,
               'deals': deals,
               'agg': agg,
               'deals_fields': deals_fields_to_show}
    return render(request, 'users/cabinet.html', context=context)


@login_required
def deal_detail(request, id: int):
    deal = get_object_or_404(UserDealInfo, id=id)
    form1 = AddStocksForm()
    if request.method == 'POST':
        form = DealInfoForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'deal_detail', args=[id])
            return HttpResponseRedirect(redirect_url)
    else:
        form = DealInfoForm(instance=deal)
    values_list = list(deal.__dict__.items())[3:]
    deal_stock = StockInfoSecurities.objects.get(secid=f'{deal.secid}')
    deal_marketdata = StockInfoMarketdata.objects.get(secid=f'{deal.secid}')
    values_securities_list = list(deal_stock.__dict__.items())[3:]
    values_marketdata_list = list(deal_marketdata.__dict__.items())[4:]

    context = {'values_list': values_list,
               'values_securities_list': values_securities_list,
               'values_marketdata_list': values_marketdata_list,
               'deal': deal,
               'form': form,
               'form1': form1}
    return render(request, 'users/deal_detail.html', context=context)

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


