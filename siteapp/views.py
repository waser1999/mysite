from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import info
from django.forms.models import model_to_dict

def index(request):
    return render(request,"select.html")

# 选中一个数据用于工作
def choose(request):
    rvalue = info.objects.all()
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        # 修改选中标记
        info.objects.all().update(ischecked = 0)
        info.objects.filter(plant = plantName).update(ischecked = 1)
    
    response = {
        'rvalue': rvalue,
    }
    return render(request,"select.html",response)

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
    return render(request,"add.html")
    # return render(request,"add.html",response)

# 删除
def delete(request):
    rvalue = info.objects.all()
    reply = ''
    try:
        if request.method == 'POST':
            plantName = request.POST.get('plant','')
            info.objects.filter(plant = plantName).delete()
            reply = 'Delete successfully'
    except:
        reply = 'Can not find object.'
    response = {
        'rvalue': rvalue,
        'reply': reply,
    }
    return render(request,"delete.html",response)

# 修改
def modify(request):
    rvalue = info.objects.all()
    reply = ''
    try:
        if request.method == 'POST':
            plantName = request.POST.get('plant','')
            column = request.POST.get('column','')          #列名
            num = request.POST.get('num','')

            info.objects.filter(plant = plantName).update(column = num)
            reply = 'Update successfully'
    except:
        reply = 'Can not find object.'
    response = {
        'rvalue': rvalue,
        'reply': reply,
    }
    return render(request,"update.html",response)

# 全部列出        
def clist(request):
    rvalue = info.objects.all()
    response = {'rvalue': rvalue}
    return render(request,"list.html", response)