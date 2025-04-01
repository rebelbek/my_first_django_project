import datetime
from django.db import models
from django.core.mail import send_mail
import uuid
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from stocks.models import Stocks, CronLogs
from notifications.models import NotificationUser
from django.db.models import Q

offset = datetime.timezone(datetime.timedelta(hours=3))


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password, **extra_fields

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    # last_name = models.CharField(verbose_name='last name', max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField('verified', default=False)
    is_receive_mail = models.BooleanField(default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    objects = UserAccountManager()
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Есть ли у пользователей конкретное разрешение?"""
        return True

    def has_module_perms(self, app_label):
        """Есть ли у пользователя разрешения на просмотр приложения `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Является ли пользователь сотрудником?"""
        # Самый простой ответ: Все администраторы - это сотрудники
        return self.is_admin

    def new_notifications(self):
        notifications = self.notificationuser_set.all()
        for notif in notifications:
            if notif.delivered is False:
                return True
        return False


class DealInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stock = models.ForeignKey(Stocks, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    buy_price = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    upper_border = models.FloatField(default=None, null=True)
    lower_border = models.FloatField(default=None, null=True)
    custom_name = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    use_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.custom_name

    @staticmethod
    def send_notification(deal, border, border_name):
        text = f'Достигнута {border_name} граница {border} для позиции {deal.custom_name} ({datetime.datetime.now(offset).strftime("%Y-%m-%d %H:%M:%S")} MSK+0 (UTC+3))'
        notification = NotificationUser(user=deal.user,
                                        text=text)
        if border_name == 'верхняя':
            deal.upper_border = None
        else:
            deal.lower_border = None
        deal.save()
        notification.save()
        if deal.user.is_receive_mail and deal.user.is_verified:
            send_mail(subject=f'Оповещение {deal.custom_name}',
                      message=text,
                      from_email='rebelbek.stocks@mail.ru',
                      recipient_list=[deal.user.email],
                      fail_silently=False)

    @classmethod
    def check_borders(cls):
        CronLogs.objects.create(func='check_borders')
        for deal in cls.objects.filter(~Q(upper_border=None) | ~Q(lower_border=None)):
            if deal.upper_border:
                if deal.stock.last >= deal.upper_border:
                    cls.send_notification(deal, deal.upper_border, 'верхняя')
            if deal.lower_border:
                if deal.stock.last <= deal.lower_border:
                    cls.send_notification(deal, deal.lower_border, 'нижняя')

