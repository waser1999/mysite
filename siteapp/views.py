from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import info

# 选中一个数据用于工作
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

# 添加一个数据
def add(request):
    if request.method == 'POST':
        # 读取设定数据
        new_plan = info(
            plantName = request.POST.get('plant',''),
            temp_u = request.POST.get('temp_u',''),
            temp_b = request.POST.get('temp_b',''),
            humi_u = request.POST.get('humi_u',''),
            humi_b = request.POST.get('humi_b',''),
            co2_u = request.POST.get('co2_u',''),
            co2_b = request.POST.get('co2_b',''),
            ischecked = request.POST.get('ischecked',''),
        )
        new_plan.save()
    return HttpResponse("Add Successsfully.")

# 删除
def delete(request):
    try:
        if request.method == 'POST':
            plantName = request.POST.get('plant','')
            info.objects.filter(plant = plantName).delete()
            response = 'Delete successfully'
    except:
        response = 'Can not find object.'
    return HttpResponse(response)

# 修改
def modify(request):
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        column = request.POST.get('column','')          #列名
        num = request.POST.get('num','')

        info.objects.filter(plant = plantName).update(column = num)
        response = 'Update successfully'
    return HttpResponse(response)

# 全部列出        
def clist(request):
    return HttpResponse(info.objects.all().order_by('ischecked'))