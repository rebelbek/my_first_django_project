from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse


@receiver(post_save, sender=User)
def user_update(sender, instance, created, *args, **kwargs):
    if created:
        send_mail(subject='Подтвердите электронную почту',
            message='Нажмите на ссылку чтобы подтвердить вашу электронную почту: '
            'http://rebelbek.ru%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            from_email='rebelbek.stocks@mail.ru',
            recipient_list=[instance.email],
            fail_silently=False,
        )