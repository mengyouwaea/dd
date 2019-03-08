from show_app.models import Book

#提供购物车中需要的数据书对象和书的数量
class CartItem():
    def __init__(self,book,amount):
        self.book=book
        self.amount=amount
#创建一个购物车类，购物车对象可以调用不同方法
class Cart():
    def __init__(self):
        self.total_price=0
        self.save_price=0
        self.cartitems=[]

    # 求总价格
    def sums(self):
        self.total_price=0
        self.save_price=0
        for i in self.cartitems:
            self.total_price1=i.book.ddpriice*i.amount
            self.save_price1=(i.book.pricing-i.book.ddpriice)*i.amount
            self.total_price+=self.total_price1
            self.save_price+=self.save_price1

    #添加购物车
    def addCart(self,bookid,num):
        for i in self.cartitems:
            if i.book.id==int(bookid):
                print(i.amount,"amount类型：",type(i.amount))
                i.amount+=num
                print("i.mount是：",i.amount)
                self.sums()
                return
        book=Book.objects.filter(id=bookid)[0]
        self.cartitems.append(CartItem(book,num))
        print(self.cartitems,"jkjjjjjjjjjjjjjj")
        self.sums()
        return

    #修改购物车
    def modifyCart(self,bookid,amount):
        for i in self.cartitems:
            if bookid==i.book.id:
                i.amount=amount
        self.sums()

#     删除购物车
    def removeCart(self,bookid):
        print("hhehehh",bookid)
        for i in self.cartitems:
            if i.book.id==bookid:
                self.cartitems.remove(i)
        print("删除后的购物车列表：",self.cartitems)
        self.sums()








