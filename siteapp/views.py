from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import info

def choose(request):
    request.encoding = 'utf-8'

    if request.method == 'POST':
        plantName = request.POST.get('plant','')
    
    # 修改选中标记
    info.objects.all().update(ischecked = 0)
    info.objects.filter(plant = plantName).update(ischecked = 1)
    
    # 传输相关参数
    refer = info.objects.get(plant = plantName)
    response = {
        'plant' : plantName,
        'temp_u' : refer.temp_u,
        'temp_b' : refer.temp_b,
        'humi_u' : refer.humi_u,
        'humi_b' : refer.humi_b,
        'co2_u' : refer.co2_u,
        'co2_b' : refer.co2_b,
        'ischecked' : refer.ischecked,
    }
    return HttpResponse(response)

# def add():

# def delete():

# def modify():

