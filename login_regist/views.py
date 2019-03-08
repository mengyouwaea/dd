import os
import random
import string

import re
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# 注册页面
from captcha.image import ImageCaptcha
from show_app.models import Users

# 注册页面显示
def regist_view(request):
    flag = request.session.get("flag")
    print("注册成功后是否有flag", flag, type(flag))
    return render(request,"register.html")
# 发送邮件方法：
def send_mail(code,email):
    subject, from_email, to = 'AI137wjl第一封测试邮件', '17310037026@sina.cn', email,
    text_content = '欢迎访问dang，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = code
    # html_content = '<p>感谢注册<a href="http://{}/lr/re_code/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000',code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
#    接收用户注册验证信息
def re_code(request):
    code=request.GET.get("code")
    if code:
        user=Users.objects.get(codes=code)
    if user:
        user.status=True
        user.save()
        return HttpResponse("验证成功")
    else:
        return HttpResponse("验证失败")
# 注册逻辑
def regist_logic(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    pwd=make_password(request.POST.get("password"))
    print(username,email,pwd)
    rules = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
    result = re.match(rules,email)
    print("result结果:", result)
    code=str(uuid.uuid4()).replace("-","")
    if result:
        user = Users(user_name=username,email=email,password=pwd,codes=code)
        user.save()
        send_mail(code,email)
        request.session["name"]=username
        request.session["email"]=email
        return redirect("lr:regist_ok")
    else:
        return HttpResponse("error")
# 注册成功页面
def regist_ok(request):
    flag = request.session.get("flag")
    print("注册成功后是否有flag", flag, type(flag))
    return render(request,"register ok.html")
# 用户名验证是否重复做异步判断
def verfiy_name(request):
    name=request.POST.get("name")
    user=Users.objects.filter(user_name=name)
    print("user:",user)
    if user:
        return HttpResponse("用户已经存在，请重新注册，或者使用用户名登录")
    else:
        return HttpResponse("可以注册")
# 邮箱验证
def verfiy_email(request):
    email=request.POST.get("email")
    user=Users.objects.filter(email=email)
    print("user:",user)
    if user:
        return HttpResponse("邮箱已经被注册！请重新输入！")
    else:
        return HttpResponse("可以注册!")
#生成验证码
def generate_captcha(request):
    image=ImageCaptcha(fonts=[os.path.abspath("captcha/segoesc.ttf")])
    code=random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,5)
    request.session["code"]="".join(code)
    data = image.generate("".join(code))
    print("".join(code))
    return HttpResponse(data, "image/png")
# 验证验证码
def verfiy_code(request):
    re_code=request.session.get("code")
    code=request.POST.get("code")
    print("code:",code,"re_code:",re_code)
    if re_code.lower()==code.lower():
        print("ok")
        return HttpResponse("验证码正确")
    return HttpResponse("验证码错误")
    print("error")
# 登录页面显示
def login_view(request):
    return render(request,"login.html")
# 登录逻辑处理
def login_logic(request):
    username = request.POST.get("username")
    remember=request.POST.get("remember")
    print("remember是记录么？",remember)
    flags=request.session.get("flag")
    if flags:
        flag=int(flags)
    else:
        flag=''
    print("flag是什么类型：",type(flag))
    res=redirect("show:index_show")
    print("登录跳转flag是：",flag)
    if username:
        if remember:
            res.set_cookie("namereme", str(username.encode("utf-8"), "latin-1"), max_age=60 * 60 * 24 * 7)
            if flag==1:
                return redirect("shopping:indent_addr")
            return res
        else:
            request.session["name"] = username
            if flag==1:
                return redirect("shopping:indent_addr")
            return res
    return redirect("lr:login_view")
# 登录时异步验证用户名或者密码是否正确
def verfiy_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = Users.objects.filter(user_name=username)
    print("username:", username, "password:", password, "user是：", user)
    if user and check_password(password,user[0].password):
        return HttpResponse("ok")
    else:
        return HttpResponse("用户名或密码错误")
# 退出
def exits(request):
    name1 = request.session.get("name")
    name2 = request.COOKIES.get("namereme")
    res=redirect("show:index_show")
    print("name1是：", name1, "name2是：", name2)
    if name1:
        del request.session["name"]
    elif name2:
        res.delete_cookie("namereme")
    return  res


