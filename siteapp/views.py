from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from .models import info, userInfo, idata
from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Model
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

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
    if -50.0 <= float(word['temp_b']) < float(word['temp_u']) <= 50.0 \
        and 0.0 <= float(word['humi_b']) < float(word['humi_u']) <= 100.0 \
        and 0 <= int(word['co2_b']) < int(word['co2_u']) \
        and 0 <= int(word['light_b']) < int(word['light_u']) \
        and 0.0 <= float(word['fei_b']) < float(word['fei_u']) <= 100.0 :
        return 1
    else:
        return 0

def index(request):
    """原始界面（登录）函数"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        user_detail = request.POST.dict()
        user = authenticate(request, **user_detail)
        if user is not None:
            login(request, user)
            return redirect('select')
        else:
            response = {"status" : -1}
            return render(request,"login.html",response)
    return render(request,"login.html")

def register(request):
    """原始界面（注册）函数，尚未完工，还需加入注册时对用户机创新表"""
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

@login_required(login_url='login.html')
def choose(request):
    """选中一个数据用于工作"""
    reply = 0
    
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        try:
            userInfo.objects.get(user = request.user.username)
        except:
            newInfo = userInfo(user = request.user.username, plant = plantName) 
            newInfo.save()
        else:
            userInfo.objects.filter(user = request.user.username).update(plant = plantName)
        reply = 1
    rvalue = info.objects.all()
    response = {
        'rvalue': rvalue,
        'status': reply,
    }
    return render(request,"select.html",response)

@login_required(login_url='login.html')
def add(request):
    """添加一个数据"""
    if not request.user.is_superuser:
        return redirect('select')
    reply = 0
    if request.method == 'POST':
        # 读取设定数据 
        try:
            new_plan = request.POST.dict()
            del new_plan['csrfmiddlewaretoken']
            for k,v in new_plan.items():
                if k in ('co2_u','co2_b','light_u','light_b'):                                # 整型数据
                    new_plan[k] = int(v)
                elif k in ('temp_u','temp_b','humi_u','humi_b','fei_u','fei_b'):              # 浮点型数据
                    new_plan[k] = round(float(v),1)
            if is_qualified(**new_plan) == 0:
                reply = 2
            else:
                info.objects.create(**new_plan)
                reply = 1
        except:
            reply = 4
        
    response = { "status": reply }
    return render(request,"add.html",response)

@login_required(login_url='login.html')
def delete(request):
    """删除数据"""
    if not request.user.is_superuser:
        return redirect('select')
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        try:
            userInfo.objects.get(plant = plantName)
        except userInfo.DoesNotExist:
            info.objects.filter(plant = plantName).delete()
            reply = 1
        else:
            reply = 3
    response = {
        'rvalue': rvalue,
        'status': reply,
    }
    return render(request,"delete.html",response)

@login_required(login_url='login.html')
def modify(request):
    """更新数据"""
    if not request.user.is_superuser:
        return redirect('select')
    rvalue = info.objects.all()
    reply = 0
    if request.method == 'POST':
        plantName = request.POST.get('plant','')
        #列名
        column = request.POST.get('column','')
        num = float(request.POST.get('num',''))

        reply = 1
        i = info.objects.filter(plant = plantName).values().get()
        if column not in ('co2_u','co2_b','light_u','light_b'):
            i[column] = round(num,1)
        else:
            i[column] = int(num)
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

@login_required(login_url='login.html')
def clist(request):
    """全部列出"""
    rvalue = info.objects.all()
    response = {'rvalue': rvalue}
    return render(request,"list.html", response)

@login_required(login_url='login.html')
def cinfo(request):
    """用户信息修改"""
    if request.method == 'POST':
        option = request.POST.get('inlineRadioOptions',)
        u = request.user
        # 修改电子邮箱地址
        if option == "option1":
            email = request.POST.get('email',)
            u.email = email
            u.save()
            response = {"status" : 1}
        # 修改密码
        elif option == "option2":
            password1 = request.POST.get('password1',)
            password2 = request.POST.get('password2',)
            if password1 != password2:
                response = {"status" : 2}
            else:
                u.set_password(password1)
                u.save()
                response = {"status" : 1}
        return render(request,"info.html",response)
    return render(request,"info.html")

@login_required(login_url='login.html')
def status(request):
    return render(request,"status.html")

@csrf_exempt                                # 去除CSRF保护
@require_http_methods("POST")
def api(request):
    """api函数实现"""
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(request, username = username, password = password)
    if user is not None:
        userInfo.objects.filter(user = username).update(status = True)
        userPlant = userInfo.objects.filter(user = username).values().get()['plant']
        rvalue = info.objects.filter(plant = userPlant)
        response = {
            'user': username,
            'value' : serializers.serialize("json",rvalue),
        }
    else:
        response = {"status" : 'Invalid User.'}
    return JsonResponse(response)

@csrf_exempt                                # 去除CSRF保护
@require_http_methods("POST")
def sendApi(request):
    """发送数据包，并发送消息(未完成）"""
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(request, username = username, password = password)
    if user is not None:
        try:
            new_data = json.loads(request.POST.get('data',''))            # data用字典形式，直接存即可
            new_data['user'] = str(username)
            idata.objects.create(**new_data)
            response = {'status' : 'Success'}
        except Exception as e:
            response = {'status' : e}
    else:
        response = {'status' : 'Invalid User.'}
    return JsonResponse(response)