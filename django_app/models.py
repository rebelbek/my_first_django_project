from django.db import models
from django.urls import reverse

# Create your models here.

class DjangoLink(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DjangoImage(models.Model):
    name = models.CharField(max_length=50, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='my_gallery/django')

    def __str__(self):
        return self.name

class DjangoInfo(models.Model):
    number = models.IntegerField(unique=True)
    chapter_name = models.CharField(max_length=55)
    text = models.TextField(blank=True)
    files = models.OneToOneField(DjangoImage, on_delete=models.PROTECT, null=True, blank=True)
    links = models.ManyToManyField(DjangoLink, blank=True)

    def __str__(self):
        return self.chapter_name

    def get_url(self):
        return reverse('chapter', args=[self.number])