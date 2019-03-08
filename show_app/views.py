import datetime

import re



from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.


# 首页展示并且取出数据展示
from show_app.models import Category, Book

# 首页
def index_show(request):
    # 左侧分类数据
    b_cate=Category.objects.filter(parent_id=0)
    s_cate=Category.objects.filter(parent_id__gt=0)
    # 新上架图书数据
    books=list(Book.objects.all().order_by("-time_shelves"))
    new_books=books[0:8]
    # 编辑推荐图书
    tj_books=list(Book.objects.filter(recommend=1))[0:8]
    # 新书热卖图书
    xr_books=list(Book.objects.all().order_by("-time_shelves","-sales"))
    # 展示前5个
    xr1=xr_books[0:5]
    xr2=xr_books[0:10]
    res=render(request,'index1.html',{"b_cate":b_cate,"s_cate":s_cate,"new_books":new_books,"tj_books":tj_books,"xr1":xr1,"xr2":xr2})
    return res
# 详情页
def book_details_page(request):
    id=request.GET.get("id")
    book_detail=Book.objects.filter(id=id)
    dz=format(book_detail[0].ddpriice/book_detail[0].pricing*10,'.2f')
    print("book_detail是：",book_detail)
    # 通过id获取这本书的类别
    category_id=book_detail[0].category_id
    #查出这本属于哪个类别
    s_n=Category.objects.filter(id=category_id)
    if s_n[0].parent_id:   #判断如果是小类别
        b_n=Category.objects.filter(id=s_n[0].parent_id) #根据小类别求出大类别
    else:
        b_n=''
    print("category_id",category_id)
    return render(request,"Book details.html",{"book_detail":book_detail,"id":id,"b_n":b_n,"s_n":s_n})
# 图书列表
def booklist_page(request):
    # 获取大类别对象
    name2 = request.COOKIES.get("namereme")
    print("name2:",name2)
    b_cate = Category.objects.filter(parent_id=0)
    # 获取小类别对象
    s_cate = Category.objects.filter(parent_id__gt=0)
    # 获取booklist中传过来的类别id判断是父类还是子类
    cid = request.GET.get("cid")
    pid = request.GET.get("pid")
    print("cid是：",cid,type(cid),"pid是：",pid)
    books=''
    l = []
    n = request.GET.get("n")
    #1、先判断类别
    # 如果是子类
    if pid!='0':
        books = Book.objects.filter(category_id=cid)
        # 通过pid,cid来获取他们的类别名称
        b_n = Category.objects.filter(id=pid)
        s_n = Category.objects.filter(id=cid)
    #如果是父类
    elif pid=='0':
    # 先利用pid查询小类，把每个对象id放入列表中方便取用
        cates=Category.objects.filter(parent_id=cid)
        print("cates:",cates)
        for cate in cates:
            l.append(cate.id)
        books = Book.objects.filter(category_id__in=l)
        # 通过pid,cid来获取他们的类别名称
        b_n = Category.objects.filter(id=cid)
        s_n=''
        print("l是：",l)
    #2、通过传递的n来判断是那种排序，直接将已经分类好的书籍进行排序即可
    if n == '1':
        books = books.order_by("-sales")
    elif n == '2':
        books = books.order_by("ddpriice")
    elif n == '3':
        books = books.order_by("-publication_time")
    else:
        n = '0'  #可用于设置默认值和默认颜色
    print("books是：",books)
    pagina=Paginator(books,per_page=3)
    print("pagina是：",pagina,"n",n)
    # 获取是第几页
    num1=request.GET.get("num")
    num2=request.GET.get("srs")
    if num1:
        num=num1
    elif num2:
        num=num2
    else:
        num=1   #设置没有传第几页默认为第一页
    page=pagina.page(num)
    lenth = len(books)
    return render(request,"booklist.html",{"b_cate":b_cate,"s_cate":s_cate,"page":page,"lenth":lenth,"cid":cid,"pid":pid,"n":n,"b_n":b_n,"s_n":s_n})


