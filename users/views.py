from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F, Value, Avg, Sum
from datetime import date, datetime
from .forms import AddStocksForm, DealInfoForm, DealSetBorderForm
from .models import DealInfo
from stocks.forms import DealForm
from stocks.models import Stocks
from notifications.models import NotificationUser
import time

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
            deal = DealInfo(user=request.user,
                            stock=stock,
                            quantity=cd['quantity'],
                            buy_price=cd['buy_price'],
                            custom_secname=stock.secname,
                            date=date.today())
            deal.save()
    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


@login_required
def stocks_add(request, id: int):
    deal = get_object_or_404(DealInfo, id=id)
    if request.method == 'POST':
        form = AddStocksForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            deal.buy_price = ((deal.buy_price * deal.quantity) +
                              (cd['buy_price'] * cd['quantity'])) / (deal.quantity + cd['quantity'])
            deal.quantity += cd['quantity']
            deal.save()
    redirect_url = reverse('deal_detail', args=[id])
    return HttpResponseRedirect(redirect_url)


@login_required
def deal_delete(request, id: int):
    deal = request.user.dealinfo_set.get(id=id)
    if request.method == 'POST':
        deal.delete()
        redirect_url = reverse('cabinet')
        return HttpResponseRedirect(redirect_url)
    else:
        context = {'deal': deal}
    return render(request, 'users/deal_delete.html', context=context)


@login_required
def cabinet(request):
    form = DealForm()
    user = request.user
    deals = user.dealinfo_set.all().annotate(
        cost=F('quantity') * F('buy_price'),
        value=F('quantity') * F('stock__last'),
        profit=F('value') - F('cost'),
    )
    notifications = user.notificationuser_set.all()
    new_notification = False
    for notif in notifications:
        if notif.delivered is False:
            new_notification = True
            break
    agg = deals.aggregate(Sum('cost'), Sum('value'), Sum('profit'))
    context = {'form': form,
               'deals': deals,
               'new_notification': new_notification,
               'agg': agg,
               'deals_fields': deals_fields_to_show}
    return render(request, 'users/cabinet.html', context=context)


@login_required
def deal_detail(request, id: int):
    deal = get_object_or_404(DealInfo, id=id)
    if request.method == 'POST':
        form = DealInfoForm(request.POST, instance=deal)
        form_set = DealSetBorderForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'deal_detail', args=[id])
            return HttpResponseRedirect(redirect_url)
        if form_set.is_valid():
            form_set.save()
            redirect_url = reverse(f'deal_detail', args=[id])
            return HttpResponseRedirect(redirect_url)
    else:
        form = DealInfoForm(instance=deal)
        form_set = DealSetBorderForm(instance=deal)
    form_add = AddStocksForm()
    values_list = list(deal.__dict__.items())[4:]
    values_stock_list = list(deal.stock.__dict__.items())[2:]
    context = {'values_list': values_list,
               'values_stock_list': values_stock_list,
               'deal': deal,
               'form': form,
               'form_set': form_set,
               'form_add': form_add}
    return render(request, 'users/deal_detail.html', context=context)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def check_border_auto():
    while True:
        for deal in DealInfo.objects.all():
            if deal.upper_border:
                if deal.stock.last >= deal.upper_border:
                    notification = NotificationUser(user=deal.user,
                                                    text=f'Достигнута верхняя граница {deal.upper_border} для позиции {deal.custom_secname}',
                                                    date=datetime.now())
                    deal.upper_border = None
                    deal.save()
                    notification.save()
            if deal.lower_border:
                if deal.stock.last <= deal.lower_border:
                    notification = NotificationUser(user=deal.user,
                                                    text=f'Достигнута нижняя граница {deal.lower_border} для позиции {deal.custom_secname}',
                                                    date=datetime.now())
                    deal.lower_border = None
                    deal.save()
                    notification.save()
        time.sleep(10)


def check_border(request):
    check_border_auto()
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)