from importlib.metadata import pass_none

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F, Value, Avg, Sum
from datetime import date
from .forms import AddStocksForm, DealInfoForm
from .models import UserDealInfo
from stocks.forms import DealForm
from stocks.models import Stocks


# Create your views here.

deals_fields_to_show = ['тикер', 'дата сделки', 'полное название', 'кол-во акций', 'цена покупки',
                        'потрачено', 'цена текущая', 'стоимость', 'прибыль', 'X']

@login_required
def deal_add(request, secid: str):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            stock = Stocks.objects.get(secid=secid)
            cd = form.cleaned_data
            deal = UserDealInfo(st=stock,
                                username=request.user.username,
                                secid=secid,
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
    if deal.username != request.user.username:
        raise Http404
    if request.method == 'POST':
        deal.delete()
        redirect_url = reverse('cabinet')
        return HttpResponseRedirect(redirect_url)
    else:
        context = {'deal' : deal}
    return render(request, 'users/deal_delete.html', context=context)


@login_required
def cabinet(request):
    form = DealForm()
    deals = UserDealInfo.objects.filter(username=request.user.username).annotate(
        cost=F('quantity') * F('buy_price'),
        value=F('quantity') * F('st__last'),
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
    deal_stock = Stocks.objects.get(secid=f'{deal.secid}')
    values_stock_list = list(deal_stock.__dict__.items())[3:]
    context = {'values_list': values_list,
               'values_stock_list': values_stock_list,
               'deal': deal,
               'form': form,
               'form1': form1}
    return render(request, 'users/deal_detail.html', context=context)

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


