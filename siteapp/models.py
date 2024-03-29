from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class info(models.Model):
    plant = models.CharField(max_length = 50, primary_key = True)
    temp_u = models.DecimalField(default=25.0, max_digits=3, decimal_places=1)      # 温度
    temp_b = models.DecimalField(default=20.0, max_digits=3, decimal_places=1)
    humi_u = models.DecimalField(default=90.0, max_digits=3, decimal_places=1)      # 湿度
    humi_b = models.DecimalField(default=50.0, max_digits=3, decimal_places=1)
    co2_u = models.IntegerField(default=1000)                       # 二氧化碳
    co2_b = models.IntegerField(default=0)
    light_u = models.IntegerField(default=500)                     # 光照
    light_b = models.IntegerField(default=10)
    fei_u = models.DecimalField(default=1.0, max_digits=3, decimal_places=1)       # 水肥浓度
    fei_b = models.DecimalField(default=0, max_digits=3, decimal_places=1)

class userInfo(models.Model):
    user = models.CharField(max_length = 50, primary_key = True)
    plant = models.CharField(max_length = 50)           # 用户选择的植物
    status = models.BooleanField(default=False)         # 用户机器开关状态(默认关)
    temp_h = models.BooleanField(default=False)         # 温度报警置位
    fei_h = models.BooleanField(default=False)          # 水肥添加置位
    error_s = models.CharField(default=0, max_length = 50)            # 机器错误状态（0为正常）
    url_address = models.CharField(blank = True, null = True, max_length = 150)

class idata(models.Model):
    user = models.CharField(max_length = 50)
    dateTime = models.DateTimeField(default=datetime.today(), primary_key = True) # 上传时间
    temp = models.DecimalField(default=25.0, max_digits=3, decimal_places=1)      # 温度
    humi = models.DecimalField(default=50.0, max_digits=3, decimal_places=1)      # 湿度
    co2 = models.IntegerField(default=1000)                                       # 二氧化碳
    light = models.IntegerField(default=500)                                    # 光照
    fei = models.DecimalField(default=0, max_digits=3, decimal_places=1)        # 水肥浓度
    error_hint = models.CharField(default=0, max_length = 50)                   # 机器错误代码