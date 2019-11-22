from django.db import models
from account.models import Users

# Create your models here.
class Scribblet(models.Model):
    user = models.ForiegnKey(Users, on_delete=models.CASCADE)
    sribbletId = models.IntegerField()
    
    name = models.CharField.max_length(64)
    target = models.CharField.max_length(10)
    language = models.CharField.max_length(3)
    content = models.CharField.max_length(1000000)

