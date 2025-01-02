from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DjangoInfo


def first_page(request):
    '''Функция для редиректа на первую страницу'''
    redirect_url = reverse('chapter', kwargs={'number':1})
    return HttpResponseRedirect(redirect_url)


def detail(request, number: int):
    chapters = DjangoInfo.objects.all()
    description = get_object_or_404(chapters, number=number)
    context = {'chapters': chapters,
               'des': description}
    return render(request, 'django_app/detail.html', context=context)
