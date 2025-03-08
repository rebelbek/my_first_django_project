from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

class NotificationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Уведомление для {self.user}, id = {self.id}'