from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Оповещение для {self.user}, id = {self.id}'