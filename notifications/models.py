from django.db import models
from django.conf import settings


# Create your models here.

class NotificationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Уведомление для {self.user}, id = {self.id}'