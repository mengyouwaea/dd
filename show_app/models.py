# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `  ` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Addr(models.Model):
    recipient = models.CharField(max_length=20,  null=True)
    recipient_addr = models.CharField(max_length=50,  null=True)
    zip = models.CharField(max_length=10, null=True)
    phone_number = models.IntegerField( null=True)
    cell_phone = models.IntegerField( null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'addr'

class BookOrder(models.Model):
    order = models.ForeignKey('YgBook', models.DO_NOTHING,  null=True)
    book_count = models.IntegerField( null=True)
    book = models.ForeignKey('Book', models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'book_order'


class Category(models.Model):
    class_name = models.CharField(max_length=20, null=True)
    parent_id = models.IntegerField(null=True)
    column_4 = models.CharField(db_column='Column_4', max_length=10, null=True)  # Field name made lowercase.
    column_5 = models.CharField(db_column='Column_5', max_length=10, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'category'


class Book(models.Model):
    author = models.CharField(max_length=20,   null=True)  #作业
    book_name = models.CharField(max_length=20,   null=True)
    summary = models.CharField(max_length=200,   null=True) #书摘插图
    custom_core = models.IntegerField(  null=True)     #顾客评分
    inventory = models.IntegerField(  null=True)   #库存
    sales = models.IntegerField(  null=True)  #销售数量
    recommend = models.IntegerField(  null=True)   #推荐
    time_shelves = models.DateField(  null=True) #上架时间
    media_reviews = models.CharField(max_length=30,   null=True)   #媒体评论
    directory = models.CharField(max_length=30,   null=True)    #目录
    author_profile = models.CharField(max_length=30,   null=True)   #作者简介
    content_intro = models.CharField(max_length=30,   null=True)   #内容简介
    edit_recom = models.CharField(max_length=100,   null=True)     #边界推荐
    saves = models.FloatField(  null=True,db_column="save")    #节省
    ddpriice = models.FloatField(  null=True)  #当当价
    pricing = models.FloatField(  null=True)   #定价
    packaging = models.CharField(max_length=20,   null=True)   #包装
    paper = models.CharField(max_length=20,   null=True)   #纸张
    format = models.CharField(max_length=20,   null=True)   #开本
    pages = models.IntegerField(  null=True)   #页数
    words = models.IntegerField(  null=True)   #字数
    #category = models.CharField(max_length=30,   null=True)   #类别
    isbn = models.IntegerField(db_column='ISBN',   null=True)  # Field name made lowercase.   isbn
    print_num = models.CharField(max_length=20,   null=True)   #印次
    printint_time = models.DateField(  null=True)    #印刷时间
    edition = models.CharField(max_length=20,   null=True)   #版次
    publication_time = models.DateField(  null=True)   #出版时间
    press = models.CharField(max_length=30,   null=True)   #出版社
    category = models.ForeignKey('Category', on_delete=models.CASCADE, db_column='category_id',null=True)  # Field renamed because of name conflict.
    column_31 = models.CharField(db_column='Column_31', max_length=10,   null=True)  # Field name made lowercase.
    column_32 = models.CharField(db_column='Column_32', max_length=10,   null=True)  # Field name made lowercase.
    column_33 = models.CharField(db_column='Column_33', max_length=10,   null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'books'



class Users(models.Model):
    email = models.CharField(max_length=30,   null=True)
    user_name = models.CharField(max_length=20,   null=True)
    password = models.CharField(max_length=20,   null=True)
    status = models.BooleanField(default=False)  # Field name made lowercase.
    codes=models.CharField(max_length=40,null=True)
    class Meta:
          
        db_table = 'users'


class YgBook(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING,null=True)
    time = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(  null=True)
    addr_name = models.CharField(max_length=30,   null=True)

    class Meta:
        db_table = 'yg_book'