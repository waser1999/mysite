from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import info
from django.forms.models import model_to_dict

# reply == 1，成功；
# reply == 0，初始值；
# reply == 2，范围值不符合规范；

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
        'status': reply,
    }
    return render(request,"select.html",response)

# 添加一个数据
def add(request):
    reply = 0
    if request.method == 'POST':
        # 读取设定数据 
        plant = request.POST.get('plant',''),
        temp_u = int(request.POST.get('temp_u','')),
        temp_b = int(request.POST.get('temp_b','')),
        humi_u = int(request.POST.get('humi_u','')),
        humi_b = int(request.POST.get('humi_b','')),
        co2_u = int(request.POST.get('co2_u','')),
        co2_b = int(request.POST.get('co2_b','')),
        if -50 <= temp_b[0] < temp_u[0] <= 50 and 0 <= humi_b[0] < humi_u[0] <= 100 and 0 <= co2_b[0] < co2_u[0] :
            new_plan = info(
                plant = plant[0],
                temp_b = temp_b[0],
                temp_u = temp_u[0],
                humi_b = humi_b[0],
                humi_u = humi_u[0],
                co2_b = co2_b[0],
                co2_u = co2_u[0],
                ischecked = 0,
            )
            new_plan.save()
            reply = 1
        else:
            reply = 2
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
        'status': reply,
    }
    return render(request,"delete.html",response)

# 更新
def modify(request):
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        column = request.POST.get('column','')        #列名
        num = int(request.POST.get('num',''))
        
        reply = 1
        i = info.objects.filter(plant = plantName).get()
        j = i.temp_u
        if column == 'temp_u' and i.temp_b < num <= 50:
            info.objects.filter(plant = plantName).update(temp_u = num)
        elif column == 'temp_b' and i.temp_u > num >= -50:
            info.objects.filter(plant = plantName).update(temp_b = num)
        elif column == 'humi_u' and i.humi_b < num <= 100:
            info.objects.filter(plant = plantName).update(humi_u = num)
        elif column == 'humi_b' and i.humi_u > num >= 0:
            info.objects.filter(plant = plantName).update(humi_b = num)
        elif column == 'co2_u' and i.co2_b < num:
            info.objects.filter(plant = plantName).update(co2_u = num)
        elif column == 'co2_b' and i.co2_u > num >= 0:
            info.objects.filter(plant = plantName).update(co2_b = num)
        else:
            reply = 2

    response = {
        'rvalue': rvalue,
        'status': reply,
    }
    return render(request,"update.html",response)

# 全部列出        
def clist(request):
    rvalue = info.objects.all().order_by("ischecked").reverse()         # ischecked选中在上的置顶，排序
    response = {'rvalue': rvalue}
    return render(request,"list.html", response)