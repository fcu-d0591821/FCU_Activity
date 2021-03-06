from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ExtendUser(AbstractUser):
    studentId = models.CharField(max_length=8)
    nickName = models.CharField(max_length=6)

class Activity(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(ExtendUser, on_delete='CASCADE')
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='', blank=True, default='default.jpg')
