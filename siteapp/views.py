from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import info
from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

# reply == 1，成功；
# reply == 0，初始值；
# reply == -1，登陆错误；
# reply == 2，范围值不符合规范；
# reply == 3，删除了已经选择的配置；
# reply == 4，植物名称重复错误。

def is_qualified(**word):
    """数据校验函数
    
    有上下界的词尾b(below)表示下界，u(upper)表示上界
    """
    if -50 <= int(word['temp_b']) < int(word['temp_u']) <= 50 \
        and 0 <= int(word['humi_b']) < int(word['humi_u']) <= 100 \
        and 0 <= int(word['co2_b']) < int(word['co2_u']) :
        return 1
    else:
        return 0

def index(request):
    """原始界面（登录）函数"""
    if request.method == 'POST':
        user_detail = request.POST.dict()
        user = authenticate(request, **user_detail)
        if user is not None:
            login(request, user)
            rvalue = info.objects.all().order_by("ischecked").reverse()
            response = {
                "username" : user.username,
                "rvalue" : rvalue,
            }
            return render(request,"select.html",response)
        else:
            response = {"status" : -1}
            return render(request,"login.html",response)
    return render(request,"login.html")

def register(request):
    """原始界面（注册）函数"""
    if request.method == 'POST':
        newUser = request.POST.dict()
        if newUser['password1'] != newUser['password2']:
            response = {"status" : 2}
        elif User.objects.filter(username = newUser['username']):
            response = {"status" : 4}
        else:
            user = User.objects.create_user(username = newUser['username'], password = newUser['password1'], email = newUser['email'])
            user.save()
            response = {"status" : 1}
        return render(request,"register.html",response)
    return render(request,"register.html")

def choose(request):
    """选中一个数据用于工作"""
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

def add(request):
    """添加一个数据"""
    reply = 0
    if request.method == 'POST':
        # 读取设定数据 
        try:
            new_plan = request.POST.dict()
            new_plan['ischecked'] = 0
            del new_plan['csrfmiddlewaretoken']
            for k,v in new_plan.items():
                if k != 'plant':
                    new_plan[k] = int(v)
            if is_qualified(**new_plan) == 0:
                reply = 2
            else:
                info.objects.create(**new_plan)
                reply = 1
        except:
            reply = 4
        
    response = { "status": reply }
    return render(request,"add.html",response)

def delete(request):
    """删除数据"""
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        if info.objects.filter(plant = plantName).get().ischecked == 0:
            info.objects.filter(plant = plantName).delete()
            reply = 1
        else:
            reply = 3
    response = {
        'rvalue': rvalue,
        'status': reply,
    }
    return render(request,"delete.html",response)

def modify(request):
    """更新数据"""
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        #列名
        column = request.POST.get('column','')
        num = int(request.POST.get('num',''))

        reply = 1
        i = info.objects.filter(plant = plantName).values().get()
        i[column] = num
        # 上下界合标判定
        if is_qualified(**i):
            info.objects.filter(plant = plantName).update(**i)
        else:
            reply = 2

    response = {
        'rvalue': rvalue,
        'status': reply,
    }
    return render(request,"update.html",response)
 
def clist(request):
    """全部列出"""
    # ischecked选中在上的置顶，排序
    rvalue = info.objects.all().order_by("ischecked").reverse()
    response = {'rvalue': rvalue}
    return render(request,"list.html", response)

def api(request):
    """api函数实现"""
    rvalue = info.objects.filter(ischecked = 1)
    response = {
        'value' : serializers.serialize("json",rvalue),
    }
    return JsonResponse(response)