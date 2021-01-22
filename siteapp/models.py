from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class info(models.Model):
    plant = models.CharField(max_length = 50, primary_key = True)
    temp_u = models.IntegerField()
    temp_b = models.IntegerField()
    humi_u = models.IntegerField()
    humi_b = models.IntegerField()
    co2_u = models.IntegerField()
    co2_b = models.IntegerField()
    # light_u = models.IntegerField()
    # light_b = models.IntegerField()

class userInfo(models.Model):
    user = models.CharField(max_length = 50, primary_key = True)
    plant = models.CharField(max_length = 50)