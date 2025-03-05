from django.shortcuts import render

from django.http import HttpResponseRedirect

# Create your views here.


def notifications(request):
    user = request.user
    all_notifications = user.notificationuser_set.order_by('-date')
    context = {'notifications': all_notifications,}
    return render(request, 'notifications/notifications.html', context=context)


def notifications_delete(request):
    user = request.user
    user.notificationuser_set.all().delete()
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)


def notification_delete(request, id: int):
    user = request.user
    notification = user.notificationuser_set.get(id = id)
    notification.delete()
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)


def notifications_read(request):
    user = request.user
    all_notifications = user.notificationuser_set.all()
    for notif in all_notifications:
        if notif.delivered is False:
            notif.delivered = True
            notif.save()
    redirect_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(redirect_url)