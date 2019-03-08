import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# 购物车显示页面,获取session中存储的bookid从而添加购物车，并添加书籍


# 展示购物车
from shop.shopcar import Cart

# 购物车展示页面
from show_app.models import Addr, YgBook, Users, BookOrder

from django.db import transaction
def show(request):
    car=request.session.get("car")
    print("show页面有购物车么？",car)
    # 判断是否有购物车
    # 有购物车
    if car:
        print("有购物车，才可以展示购物车内容")
        books_list = car.cartitems
        total_price=car.total_price
        save_price=car.save_price
        length=len(books_list)
        print("length是：",length)
        print("books_list是什么？", books_list,total_price,save_price)
    else:
        books_list=''
        total_price=''
        save_price=''
        length=0
    return render(request, "car.html", {"books_list": books_list,"total_price":total_price,"save_price":save_price,"length":length})

#增加购物车
#接收书籍列表页面购买的bookid，判断购买的哪个书籍
def add(request):
    #接收传过来的bookid
    bookid = int(request.GET.get("bookid"))
    num=int(request.GET.get("num"))
    print("booklist购买的哪本书：",bookid,num)
    #从session中获取购物车，并判断购物车是否存在
    car=request.session.get("car")
    print("增加的购物车对象是：",car)
    # 如果存在直接调用购物车中方法
    if car:
        car.addCart(bookid,num)
        request.session["car"]=car
        print("11111111111")
    # 如果不存在，初始化购物车对象，并调用addCart方法，添加购物车，并把购物车对象存入session
    else:
        print("222222222222")
        cart=Cart()
        cart.addCart(bookid,num)
        request.session["car"]=cart
        print("cart是什么：",cart)
    return  HttpResponse("booklist buy ok")

# 修改购物车
def modify(request):
    #接收参数
    bookid=int(request.GET.get("bookid"))
    amount=int(request.GET.get("amount"))
    print("bookid是多少",bookid,"amount是什么：",amount)
    #获取购物车对象
    cart=request.session.get("car")
    #调用购物车修改方法：
    cart.modifyCart(bookid,amount)
    #重新储存购物车对象
    request.session["car"]=cart
    total_price=cart.total_price
    save_price=cart.save_price
    print("total_price是：",total_price,"save_price是：",save_price)
    return JsonResponse({"total_price":total_price,"save_price":save_price})

#删除购物车
def remove(request):
    #获取购物车对象直接调用购物车的删除方法
    car=request.session.get("car")
    bookid=int(request.GET.get("bookid"))
    print("获取要删除car:",car,"bookid:",bookid)
    car.removeCart(bookid)
    request.session["car"]=car
    total_price=car.total_price
    save_price=car.save_price
    length=len(car.cartitems)
    print("长度：",length)
    print("删除后的总价：",total_price,"删除后节省:",save_price)
    return JsonResponse({"total_price":total_price,"save_price":save_price,"length":length})

#结算订单验证用户是否登录
def settlement(request):
    name1=request.session.get("name")
    name2=request.COOKIES.get("namereme")
    flag=request.GET.get("flag")
    request.session["flag"]=flag
    if name1 or name2:
        return redirect("shopping:indent_addr")
    else:
        return redirect("lr:login_view")

# 订单地址生成页面需要获取订单信息，进行展示购物信息和价格
def indent_addr(request):
    #获取购物车信息传入模板供展示已购买商品
    car=request.session.get("car")
    print("生成订单时，获取的购物信息",car)
    username1=request.session.get("name")
    username2=request.COOKIES.get("namereme")
    if username1:
        username=username1
    elif username2:
        username=username2
    if username:
        user = Users.objects.filter(user_name=username)
    #查询地址表中的信息，并传入模板，供模板地址异步显示使用
        addrs=Addr.objects.filter(user_id=user[0].id)
    else:
        addrs=''
    print("查询到的addrs是：",addrs)
    return render(request,"indentaddr.html",{"car":car,"addrs":addrs})

#动态生成地址
def auto_addr(request):
    id=request.POST.get("id")
    print("id:",id)
    if id:
        addr=list(Addr.objects.filter(id=id).values())
    else:
        addr=None
    print("动态addr对象：",addr)
    return JsonResponse({"addr":addr})

# 订单生成成功页面
def indent_ok(request):
    recipient=request.POST.get("recipient")
    detail_addr=request.POST.get("detail_addr")
    phone_number=request.POST.get("phone_number")
    rules1='[1-9]\d{5}(?!\d)'#邮政编码格式验证
    zips=request.POST.get("zip")
    rules2='^[1][3,4,5,7,8,9][0-9]{9}$' #手机号码格式验证
    cell_phone=request.POST.get("cell_phone")
    print("联系人：",recipient,"详细地址：",detail_addr,"电话：",phone_number,"邮政编码：",zips,"手机：",cell_phone)
    #获取select的value值，如果为空的时候保存这些数据
    values=request.POST.get("address")
    print("获取到的select的value是",values)
    #获取购物车信息
    car=request.session.get("car")
    username1=request.session.get("name")
    username2=request.COOKIES.get("namereme")
    print("购物车：",car,"用户1：",username1,"用户2:",username2)
    #用户订单中记录用户购买订单需要获取用户名信息
    username=''
    if username1:
        username=username1
    elif username2:
        username=username2
    print("username最后是：",username)
    #获取用户的id
    user=Users.objects.filter(user_name=username)[0]
    id=user.id
    print("获取到用户的id是：",id)
#用户电话可为空，设置默认为空
    if phone_number=='':
        phone_number=None
    try:
        with transaction.atomic():
            print("判断之前进入了事务么？")
            print(re.match(rules1,zips),re.match(rules2,cell_phone))

            if re.match(rules1,zips) and re.match(rules2,cell_phone):
                print("是否已经进入事务")
                if values == '':
                    #满足的时候才可以存储用户的地址信息
                    addr=Addr(recipient=recipient,recipient_addr=detail_addr,zip=zips,cell_phone=cell_phone,phone_number=phone_number,user_id=id)
                    print("addr")
                    addr.save()
                    print("addr存储：",addr)
                #存储用户订单信息用户购买的书籍总价以及地址
                yg_book=YgBook(total_price=car.total_price,addr_name=detail_addr,user_id=id)
                yg_book.save()
                # 把订单id,订单数量，总价存入session供订单成功页面显示
                request.session['order_id']=yg_book.id
                request.session["count"]=len(car.cartitems)
                request.session["price"]=car.total_price
                print("yg_book存储：",yg_book)
                #存储用户购买了哪些书籍以及与订单信息绑定的id
                for i in car.cartitems:
                    print("不能进入for循环？")
                    book_order=BookOrder(book_count=i.amount,book_id=i.book.id,order_id=yg_book.id)
                    print("是存储的问题么？")
                    book_order.save()
                    print("book_order存储：", book_order)
                #订单生成成功要把购物车清空，删除购物车
                del request.session["car"]
    except:
        print("error")
        return render(request,"error.html")
    return render(request, "indent ok.html")






