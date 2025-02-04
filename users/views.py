from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from .forms import AddStocksForm, DealInfoForm, DealSetBorderForm
from .models import DealInfo
from datetime import datetime
from stocks.forms import DealForm
from stocks.models import Stocks
from stocks.scripts.make_reports import ReportsMaker

# Create your views here.

date_today = datetime.today().strftime('%d-%m-%Y')
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
                            custom_secname=stock.secname)
            deal.save()
    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


@login_required
def stocks_add(request, pk: int):
    deal = get_object_or_404(DealInfo, pk=pk)
    if request.method == 'POST':
        form = AddStocksForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            deal.buy_price = ((deal.buy_price * deal.quantity) +
                              (cd['buy_price'] * cd['quantity'])) / (deal.quantity + cd['quantity'])
            deal.quantity += cd['quantity']
            deal.save()
    redirect_url = reverse('deal_detail', args=[pk])
    return HttpResponseRedirect(redirect_url)


@login_required
@require_http_methods(['DELETE'])
def deal_delete(request, pk: int):
    deal = request.user.dealinfo_set.get(pk=pk)
    deal.delete()
    return HttpResponse()


@login_required
def cabinet(request):
    form = DealForm()
    user = request.user
    deals = user.dealinfo_set.all().annotate(
        cost=F('quantity') * F('buy_price'),
        value=F('quantity') * F('stock__last'),
        profit=F('value') - F('cost'),
    )
    new_notification = user.new_notifications()
    agg = deals.aggregate(Sum('cost'), Sum('value'), Sum('profit'))
    context = {'form': form,
               'deals': deals,
               'new_notification': new_notification,
               'agg': agg,
               'deals_fields': deals_fields_to_show}
    return render(request, 'users/cabinet.html', context=context)


@login_required
def deal_detail(request, pk: int):
    deal = get_object_or_404(DealInfo, pk=pk)
    if request.method == 'POST':
        form = DealInfoForm(request.POST, instance=deal)
        form_set = DealSetBorderForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            redirect_url = reverse(f'deal_detail', args=[pk])
            return HttpResponseRedirect(redirect_url)
        if form_set.is_valid():
            form_set.save()
            redirect_url = reverse(f'deal_detail', args=[pk])
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
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def reports(request):
    return render(request, 'users/reports.html')


@login_required
def get_reports(request, model: str, format_file: str):
    if model not in ['stocks', 'deals'] and format_file not in ['html', 'pdf', 'csv', 'xlsx']:
        return Http404
    filename = f'{model}_{date_today}.{format_file}'
    reports_path = f'reports/{format_file}/{filename}'
    stocks_content_fields = ['№', 'Тикер', 'Полное название', 'Кол-во акций',
                             'Размер лота', 'Цена 1 акции']
    deals_content_fields = ['№', 'Тикер', 'Кол-во акций', 'Цена покупки',
                            'Потрачено', 'Стоимость', 'Прибыль']
    if model == 'stocks':
        values = list(Stocks.objects.all().values_list('secid', 'secname', 'issuesize', 'lotsize', 'last'))
        ReportsMaker(values, stocks_content_fields, model, format_file, reports_path).write_to_file()
    if model == 'deals':
        deals = request.user.dealinfo_set.all().annotate(
            secid=F('stock__secid'),
            cost=F('quantity') * F('buy_price'),
            value=F('quantity') * F('stock__last'),
            profit=F('value') - F('cost'),
            ).values_list('secid', 'quantity', 'buy_price', 'cost', 'value', 'profit')
        values = [[round(i, 2) if isinstance(i, float) else i for i in deal] for deal in deals]
        additional = deals.aggregate(Sum('cost'), Sum('value'), Sum('profit'))
        ReportsMaker(values, deals_content_fields, model, format_file, reports_path, additional).write_to_file()
    file = open(reports_path, 'rb')
    # return FileResponse(file, as_attachment=True, filename=filename)
    response = HttpResponse(file.read(), content_type=f'application/{format_file}')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    file.close()
    return response