from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import DealForm
from .models import UserDealInfo
from stocks.models import StockInfoSecurities
from datetime import date

deals_fields_to_show = ['тикер', 'полное название', 'кол-во акций', 'цена покупки', 'цена сейчас']

# Create your views here.


def home(request):
    return render(request, 'users/home.html')


def add_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            stock = StockInfoSecurities.objects.get(secid=cd['secid'].upper())
            deal = UserDealInfo(stock = stock,
                                username=request.user.username,
                                secid=cd['secid'].upper(),
                                quantity=cd['quantity'],
                                buy_price=cd['buy_price'],
                                date=date.today())
            deal.save()

    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


@login_required
def cabinet(request):
    form = DealForm()
    deals = UserDealInfo.objects.filter(username = request.user.username)
    context = {'form': form,
               'deals': deals,
               'deals_fields': deals_fields_to_show}
    return render(request, 'users/cabinet.html', context=context)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

