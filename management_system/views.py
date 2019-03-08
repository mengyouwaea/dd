import datetime
from show_app.models import Category, Addr, Book, YgBook, Users
from decimal import Decimal
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
# 总index系统显示
def index(request):
    return render(request,'management_index.html')

#增加书籍展现
def add_books(request):
    cates=Category.objects.filter(parent_id__gt=0)
    print("cates:",cates)
    return render(request,'main/add_books.html',{"cates":cates})

def add_books_logic(request):
    name = request.POST.get("book_name")
    print("name:",name)
    author = request.POST.get("author")
    press = request.POST.get("press")
    cate_id = request.POST.get("cate")
    print("cate_id:", cate_id)
    inventory = request.POST.get("inventory")
    sales = request.POST.get("sales")
    recommend = request.POST.get("recommend")
    time = request.POST.get("time_shelves")
    if (time):
        time_shelves = datetime.datetime.strptime(time, '%Y-%m-%d')
        print("time_shelves:",time_shelves,type(time_shelves))
    ddprice = request.POST.get("ddprice")
    price = request.POST.get("price")
    if cate_id:
         # 查出类别对象
        cates = Category.objects.get(id=int(cate_id))
        print("cates类a别对象：",cates)
        print(author,name,press,cates,inventory,sales,recommend,time_shelves,ddprice,price)
        book=Book.objects.create(author=author, book_name=name,
                                  press=press,category=cates, inventory=int(inventory),
                                  sales=int(sales),recommend=int(recommend),time_shelves=time_shelves,
                                  ddpriice=Decimal(ddprice), pricing=Decimal(price))
        book.save()
    print("怎么出错了呢")
    return redirect("management_system:add_books")


#书籍列表显示所有书籍
def books_list(request):
    books1=Book.objects.all()
    length=len(books1)
    #创建page对象
    pagina=Paginator(books1,per_page=3)
    num1=request.GET.get("num")
    print("num1:", num1, type(num1))
    if num1==None:
        num=1
    else:
        num=num1

    page=pagina.page(num)
    return render(request,'main/books_list.html',{"page":page,"length":length})

# 删除图书
def del_book(request):
    id=request.GET.get("id")
    print("id传过来：",id)
    Book.objects.get(id=id).delete()
    return redirect("management_system:books_list")


#增加父类别展示
def add_parent_cate(request):
    return render(request,'main/parent_category.html')
# 增加父类别逻辑
def add_parent_logic(request):
    parent_cate=request.POST.get("add_parent")
    print("parent_cate:",parent_cate)
    Category(class_name=parent_cate,parent_id=0).save()
    return redirect("management_system:add_parent_cate")
# 增加子类别
def add_child_cate(request):
    cates=Category.objects.filter(parent_id=0)
    return render(request,'main/child_cate.html',{"cates":cates})

# 增加子类别逻辑
def add_chile_cate_logic(request):
    #获取类别数据
    child_name=request.POST.get("child_name")
    parent_id=request.POST.get("xz_parent")
    print("child_name:",child_name,"parent_id:",parent_id)
    if parent_id:
        Category(class_name=child_name,parent_id=int(parent_id)).save()
    return redirect("management_system:add_child_cate")

# 商品的所有类别展示
def all_cate(request):
    cates=Category.objects.all()
    b_c=Category.objects.filter(parent_id=0)
    return render(request,'main/book_catelist.html',{"cates":cates,"b_c":b_c})

# 地址列表
def address(request):
    addrs=Addr.objects.all()
    return render(request,"main/address_list.html",{"addrs":addrs})

#订单列表展示
def order_list(request):
    orders=YgBook.objects.all()
    users=Users.objects.all()
    print("users:",users)
    return render(request,'main/order_list.html',{"orders":orders,"users":users})


