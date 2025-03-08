import datetime
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, UserMailForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from .forms import AddStocksForm, DealInfoForm, DealSetBorderForm
from .models import DealInfo, User
from stocks.forms import DealForm
from stocks.models import Stocks
from stocks.scripts.make_reports import ReportsMaker

# Create your views here.


offset = datetime.timezone(datetime.timedelta(hours=3))
date_today = datetime.datetime.today().strftime('%d-%m-%Y')

def check_borders(request):
    DealInfo.check_borders()
    redirect_url = reverse('cabinet')
    return HttpResponseRedirect(redirect_url)


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
                            custom_name=stock.shortname)
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
    user = request.user
    form = DealForm()
    if request.method == 'POST':
        form_user_mail = UserMailForm(request.POST, instance=user)
        if form_user_mail.is_valid():
            form_user_mail.save()
            redirect_url = reverse('cabinet')
            return HttpResponseRedirect(redirect_url)
    else:
        form_user_mail = UserMailForm(instance=user)
    deals = user.dealinfo_set.all().annotate(
        cost=F('quantity') * F('buy_price'),
        value=F('quantity') * F('stock__last'),
        profit=F('value') - F('cost'),
    )
    new_notification = user.new_notifications()
    agg = deals.aggregate(Sum('cost'), Sum('value'), Sum('profit'))
    date_moscow = datetime.datetime.now(offset)
    context = {'form': form,
               'user': user,
               'deals': deals,
               'form_user_mail': form_user_mail,
               'new_notification': new_notification,
               'agg': agg,
               'msc_time': date_moscow}
    return render(request, 'users/cabinet.html', context=context)


@login_required
def deal_detail(request, pk: int):
    deal = get_object_or_404(DealInfo, pk=pk)
    if request.method == 'POST':
        form = DealInfoForm(request.POST, instance=deal)
        form_set = DealSetBorderForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            redirect_url = reverse('deal_detail', args=[pk])
            return HttpResponseRedirect(redirect_url)
        if form_set.is_valid():
            form_set.save()
            redirect_url = reverse('deal_detail', args=[pk])
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


class MyPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"


def send_email_to_verify(request):
    user = request.user
    send_mail(subject='Подтвердите электронную почту',
              message='Нажмите на ссылку чтобы подтвердить вашу электронную почту: '
                      'http://rebelbek.ru%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
              from_email='rebelbek.stocks@mail.ru',
              recipient_list=[user.email],
              fail_silently=False)
    redirect_url = reverse('send_email_to_verify_done')
    return HttpResponseRedirect(redirect_url)


def send_email_to_verify_done(request):
    return render(request, 'users/send_email_to_verify_done.html')

def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("Пользователь не существует или уже создан")

    user.is_verified = True
    user.save()
    return render(request, 'registration/activate.html')


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
    with  open(reports_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=f'application/{format_file}')
        response['Content-Disposition'] = f'attachment; filename={filename}'
    return response