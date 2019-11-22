from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class Scribblet(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sribbletId = models.IntegerField()
    
    name = models.CharField(max_length=64)
    target = models.CharField(max_length=10)
    language = models.CharField(max_length=3)
    content = models.CharField(max_length=1000000)

