from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import info
from django.forms.models import model_to_dict

# 选中一个数据用于工作
def choose(request):
    rvalue = info.objects.all().order_by("ischecked").reverse()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        # 修改选中标记
        info.objects.all().update(ischecked = 0)
        info.objects.filter(plant = plantName).update(ischecked = 1)
        reply = 1
    
    response = {
        'rvalue': rvalue,
        'reply': reply,
    }
    return render(request,"select.html",response)

# 添加一个数据
def add(request):
    reply = 0
    if request.method == 'POST':
        # 读取设定数据 
        new_plan = info(
            plant = request.POST.get('plant',''),
            temp_u = request.POST.get('temp_u',''),
            temp_b = request.POST.get('temp_b',''),
            humi_u = request.POST.get('humi_u',''),
            humi_b = request.POST.get('humi_b',''),
            co2_u = request.POST.get('co2_u',''),
            co2_b = request.POST.get('co2_b',''),
            ischecked = 0,
        )
        new_plan.save()
        reply = 1
    response = { "status": reply }
    return render(request,"add.html",response)

# 删除
def delete(request):
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        info.objects.filter(plant = plantName).delete()
        reply = 1
    response = {
        'rvalue': rvalue,
        'reply': reply,
    }
    return render(request,"delete.html",response)

# 更新
def modify(request):
    rvalue = info.objects.all()
    reply = 0
    try:
        if request.method == 'POST':
            plantName = request.POST.get('plant','')
            column = request.POST.get('column','')          #列名
            num = request.POST.get('num','')

            if column == 'temp_u':
                info.objects.filter(plant = plantName).update(temp_u = num)
            elif column == 'temp_b':
                info.objects.filter(plant = plantName).update(temp_b = num)
            elif column == 'humi_u':
                info.objects.filter(plant = plantName).update(humi_u = num)
            elif column == 'humi_b':
                info.objects.filter(plant = plantName).update(humi_b = num)
            elif column == 'co2_u':
                info.objects.filter(plant = plantName).update(co2_u = num)
            elif column == 'co2_b':
                info.objects.filter(plant = plantName).update(co2_b = num)
            reply = 1
                
    except:
        pass
    response = {
        'rvalue': rvalue,
        'reply': reply,
    }
    return render(request,"update.html",response)

# 全部列出        
def clist(request):
    rvalue = info.objects.all().order_by("ischecked").reverse()         # ischecked选中在上的置顶，排序
    response = {'rvalue': rvalue}
    return render(request,"list.html", response)