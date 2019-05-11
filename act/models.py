from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class ExtendUser(AbstractUser):
    studentId = models.CharField(max_length=8)
    nickName = models.CharField(max_length=6)
    # role stu 一般學生 staff 幹部 admin 管理者

class Activity(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(ExtendUser, on_delete='CASCADE')
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=10)
    poster = models.ImageField(upload_to='upload', blank=True, default='upload/default.jpg')
    